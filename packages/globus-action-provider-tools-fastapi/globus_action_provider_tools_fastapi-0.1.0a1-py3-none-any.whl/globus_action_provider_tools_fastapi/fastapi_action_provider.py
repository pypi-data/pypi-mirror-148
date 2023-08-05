import inspect
from abc import ABC, abstractmethod
from enum import Enum
from functools import partial
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

import arrow
from fastapi import BackgroundTasks, Depends, FastAPI, Header, Request, Response
from fastapi import status as fastapi_status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from globus_action_provider_tools import (
    ActionProviderDescription,
    ActionRequest,
    ActionStatus,
    ActionStatusValue,
    AuthState,
    TokenChecker,
)
from globus_action_provider_tools.authorization import (
    authorize_action_access_or_404,
    authorize_action_management_or_404,
)
from globus_action_provider_tools.errors import AuthenticationError
from globus_sdk import ConfidentialAppAuthClient
from pydantic import create_model

from .fastapi_action_provider_exceptions import (
    ActionConflictException,
    ActionMethodMissingImplementation,
    ActionNotFoundException,
    ApplicationError,
    UnauthorizedException,
)

T = TypeVar("T")
partial_return = Union[T, Awaitable[T]]

StatusInOutCallable = Callable[
    [ActionStatus], Union[ActionStatus, Awaitable[ActionStatus]]
]

_EMPTY_STATUS_DETAILS = "EMPTY STATUS MUST BE FILLED IN"


class ImplementationBehavior(Enum):
    REQUIRED = 1
    REQUIRED_WITHOUT_BACKEND = 2
    NOT_REQUIRED = 3
    UNKNOWN_METHOD = 4


_api_method_required_policies = {
    "run": ImplementationBehavior.REQUIRED,
    "status": ImplementationBehavior.REQUIRED_WITHOUT_BACKEND,
    "cancel": ImplementationBehavior.NOT_REQUIRED,
    "release": ImplementationBehavior.REQUIRED_WITHOUT_BACKEND,
    "resume": ImplementationBehavior.NOT_REQUIRED,
    "log": ImplementationBehavior.NOT_REQUIRED,
}


def _authorize_access(
    checker_function: Callable[[ActionStatus, AuthState], None],
    action: Optional[ActionStatus],
    auth_state: AuthState,
    req_action_id: str = "<Unknown>",
    raise_on_missing_action=True,
    exception_class=ActionNotFoundException,
):
    if action is None and raise_on_missing_action:
        raise exception_class(req_action_id)
    if action is not None:
        try:
            checker_function(action, auth_state)
        except AuthenticationError:
            raise exception_class(action.action_id)


def authorize_action_access(
    action: Optional[ActionStatus],
    auth_state: AuthState,
    req_action_id: str = "<Unknown>",
    raise_on_missing_action=True,
    exception_class=ActionNotFoundException,
):
    _authorize_access(
        authorize_action_access_or_404,
        action,
        auth_state,
        req_action_id=req_action_id,
        raise_on_missing_action=raise_on_missing_action,
        exception_class=exception_class,
    )


def authorize_action_management(
    action: Optional[ActionStatus],
    auth_state: AuthState,
    req_action_id: str = "<Unknown>",
    raise_on_missing_action=True,
    exception_class=ActionNotFoundException,
):
    _authorize_access(
        authorize_action_management_or_404,
        action,
        auth_state,
        req_action_id=req_action_id,
        raise_on_missing_action=raise_on_missing_action,
        exception_class=exception_class,
    )


def fill_action_status(
    in_action: ActionStatus,
    req: Optional[ActionRequest] = None,
    auth_state: Optional[AuthState] = None,
) -> ActionStatus:
    if auth_state is not None:
        in_action.creator_id = auth_state.effective_identity

    if req is not None:
        if not in_action.monitor_by and req.monitor_by:
            in_action.monitor_by = req.monitor_by
        if not in_action.manage_by and req.manage_by:
            in_action.manage_by = req.manage_by
    if in_action.is_complete() and in_action.completion_time is None:
        in_action.completion_time = str(arrow.utcnow())
    if in_action.release_after is None:
        #        in_action.release_after = datetime.timedelta(days=30)
        in_action.release_after = "P30D"
    if in_action.display_status is None:
        in_action.display_status = str(in_action.status)

    return in_action


def missing_handler(
    route_name: str,
    backend_present: bool,
    *args,
    action_request: Optional[ActionRequest] = None,
    auth_state: Optional[AuthState] = None,
    **kwargs,
) -> Optional[ActionStatus]:
    behavior = _api_method_required_policies.get(
        route_name, ImplementationBehavior.UNKNOWN_METHOD
    )
    if behavior is ImplementationBehavior.REQUIRED or (
        behavior is ImplementationBehavior.REQUIRED_WITHOUT_BACKEND
        and backend_present is False
    ):
        raise ActionMethodMissingImplementation(route_name)
    # Since a common pattern is ActionStatus in the input list and an expected
    # ActionStatus return, we find it in the args list and return it if present
    for arg in args:
        if isinstance(arg, ActionStatus):
            return fill_action_status(arg, action_request, auth_state)
    return None


async def check_token(
    checker: TokenChecker, authorization_header: Optional[str] = None
) -> AuthState:

    token = ""
    if authorization_header is not None:
        authorization_header = authorization_header.strip()
        if authorization_header.startswith("Bearer "):
            token = authorization_header.lstrip("Bearer ")

    auth_state = checker.check_token(token)
    return auth_state


def globus_auth_dependency(
    token_checker: TokenChecker,
) -> Callable[[Optional[str]], Awaitable[AuthState]]:
    async def token_checker_dependency(
        authorization: Optional[str] = Header(None),
    ) -> AuthState:
        return await check_token(token_checker, authorization)

    return token_checker_dependency


async def async_invoke(
    func: Callable[[Any], Union[T, Coroutine[Any, Any, T]]], *args, **kwargs
) -> Awaitable[T]:
    sig = inspect.signature(func)
    call_args: List[Any] = []
    call_kwargs: Dict[str, Any] = {}
    args_index = 0
    for param_name, param_info in sig.parameters.items():
        if param_name in kwargs:
            call_kwargs[param_name] = kwargs[param_name]
        elif param_info.kind in {
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.POSITIONAL_ONLY,
        }:
            if args_index < len(args):
                call_args.append(args[args_index])
                args_index += 1
        elif param_info.kind is inspect.Parameter.VAR_KEYWORD:
            call_kwargs[param_name] = kwargs
        elif param_info.kind is inspect.Parameter.VAR_POSITIONAL:
            call_args.extend(args[args_index:])
            args_index = len(args)

    if inspect.iscoroutinefunction(func):
        r = await func(*call_args, **call_kwargs)
    else:
        r = func(*call_args, **call_kwargs)
    return r


ActionProviderPersistenceReturnType = Tuple[
    Optional[ActionStatus], Optional[ActionRequest], Optional[Dict[str, Any]]
]


class ActionProviderPersistence(ABC):
    @abstractmethod
    async def lookup_by_action_id(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        ...

    @abstractmethod
    async def lookup_by_request_id_and_identity(
        self, request_id: str, user_identity: str
    ) -> ActionProviderPersistenceReturnType:
        ...

    @abstractmethod
    async def store_action(
        self,
        action: ActionStatus,
        request: Optional[ActionRequest] = None,
        creator_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> ActionProviderPersistenceReturnType:
        ...

    @abstractmethod
    async def remove_action(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        ...


class FastAPIActionProvider(FastAPI):
    def __init__(
        self,
        ap_description: ActionProviderDescription,
        globus_auth_client_id: str,
        globus_auth_client_secret: str,
        *args,
        persistence_backend: Optional[ActionProviderPersistence] = None,
        additional_scopes: Iterable[str] = (),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.auth_client = ConfidentialAppAuthClient(
            globus_auth_client_id, globus_auth_client_secret
        )
        self.ap_description = ap_description
        self.persistence_backend = persistence_backend
        self.handlers = {
            k: partial(missing_handler, k, self.persistence_backend is not None)
            for k in _api_method_required_policies.keys()
        }

        scopes = [ap_description.globus_auth_scope]
        scopes.extend(additional_scopes)
        self.token_checker = self._create_token_checker(
            globus_auth_client_id, globus_auth_client_secret, scopes
        )

        self.register_api_routes()

    def _create_token_checker(
        self,
        globus_auth_client_id: str,
        globus_auth_client_secret: str,
        scopes: Iterable[str],
    ):
        return TokenChecker(globus_auth_client_id, globus_auth_client_secret, scopes)

    def register_api_routes(self) -> None:
        ThisActionRequest = create_model(
            "ThisActionRequest",
            __base__=ActionRequest,
            body=(self.ap_description.input_schema, ...),
        )

        auth_state_dependency = Depends(globus_auth_dependency(self.token_checker))

        async def globus_auth_dependency_closure(
            authorization: Optional[str] = Header(None),
        ) -> AuthState:
            return await check_token(self.token_checker, authorization)

        @self.get("/")
        async def introspect(
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionProviderDescription:
            return await self.introspect_handler(auth_state)

        @self.post("/run", status_code=fastapi_status.HTTP_202_ACCEPTED)
        async def run(
            req: ThisActionRequest,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            status = await self.run_handler(
                req, auth_state, request, response, background_tasks
            )
            return status

        @self.get("/{action_id}/status")
        async def status(
            action_id: str,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            return await self.status_handler(
                action_id, auth_state, request, response, background_tasks
            )

        @self.post("/{action_id}/resume")
        async def resume(
            action_id: str,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            return await self.resume_handler(
                action_id, auth_state, request, response, background_tasks
            )

        @self.post("/{action_id}/cancel")
        async def cancel(
            action_id: str,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            return await self.cancel_handler(
                action_id, auth_state, request, response, background_tasks
            )

        @self.post("/{action_id}/release")
        async def release(
            action_id: str,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            return await self.release_handler(
                action_id, auth_state, request, response, background_tasks
            )

        @self.get("/{action_id}/log")
        async def log(
            action_id: str,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks,
            auth_state: AuthState = auth_state_dependency,
        ) -> ActionStatus:
            return await self.log_handler(
                action_id, auth_state, request, response, background_tasks
            )

    def create_stub_action_status(
        self, action_id: Optional[str], creator_id: Optional[str]
    ) -> ActionStatus:
        action_props = dict(
            status=ActionStatusValue.ACTIVE,
            creator_id=creator_id,
            details=_EMPTY_STATUS_DETAILS,
        )
        if action_id is not None:
            action_props["action_id"] = action_id
        return ActionStatus(**action_props)

    async def lookup_status(
        self, action_id: str, raise_on_not_found=True
    ) -> ActionProviderPersistenceReturnType:
        if self.persistence_backend is None:
            return (None, None, None)
        (
            status,
            request,
            extra_data,
        ) = await self.persistence_backend.lookup_by_action_id(action_id)
        if status is None:
            if raise_on_not_found:
                raise ActionNotFoundException(action_id)
            status = (self.create_stub_action_status(action_id, None),)
        return status, request, extra_data

    async def lookup_by_request_id(
        self, request_id: str, creator_id: str
    ) -> ActionProviderPersistenceReturnType:
        if self.persistence_backend is None:
            return (None, None, None)
        (
            status,
            request,
            extra_data,
        ) = await self.persistence_backend.lookup_by_request_id_and_identity(
            request_id, creator_id
        )
        if status is None:
            status = self.create_stub_action_status(None, creator_id)
        return status, request, extra_data

    async def introspect_handler(self, auth_state: AuthState) -> JSONResponse:
        if not auth_state.check_authorization(
            self.ap_description.visible_to, allow_public=True
        ):
            raise UnauthorizedException()

        def model_class_encoder(model_class) -> Dict:
            r = model_class.schema()
            return r

        json_vals = jsonable_encoder(
            self.ap_description,
            custom_encoder={
                type(self.ap_description.input_schema): model_class_encoder
            },
        )
        return JSONResponse(content=json_vals)

    async def run_handler(
        self,
        req: ActionRequest,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        if not auth_state.check_authorization(
            self.ap_description.runnable_by, allow_all_authenticated_users=True
        ):
            raise UnauthorizedException()
        status, saved_req, extra_data = await self.lookup_by_request_id(
            req.request_id, auth_state.effective_identity
        )
        if saved_req is not None:
            if saved_req.body != req.body:
                raise ActionConflictException(
                    saved_req.request_id,
                    (
                        f"Request with id {saved_req.request_id} with different body "
                        "payload already processed"
                    ),
                )
            elif status is not None:
                return await self.status_handler(
                    status.action_id, auth_state, request, response, background_tasks
                )
            else:
                raise ApplicationError(
                    "Unable to find action associated with request id "
                    f"{saved_req.request_id}"
                )
        if extra_data is None:
            extra_data = {}
        status = await async_invoke(
            self.handlers["run"],
            req,
            action_status=status,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        status = fill_action_status(status, req, auth_state)
        if self.persistence_backend is not None and status is not None:
            await self.persistence_backend.store_action(
                status, req, auth_state.effective_identity, extra_data
            )
        return status

    async def status_handler(
        self,
        action_id: str,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        status, req, extra_data = await self.lookup_status(action_id)
        authorize_action_access(status, auth_state)
        if status is not None and status.is_complete():
            return status
        res = await async_invoke(
            self.handlers["status"],
            status,
            action_status=status,
            action_id=action_id,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        res = fill_action_status(res, req, auth_state)
        if self.persistence_backend is not None and status is not None:
            await self.persistence_backend.store_action(
                status, req, auth_state.effective_identity, extra_data
            )
        return res

    async def release_handler(
        self,
        action_id: str,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        status, req, extra_data = await self.lookup_status(action_id)
        authorize_action_management(status, auth_state)
        if status is not None and not status.is_complete():
            raise ActionConflictException(
                action_id,
                detail="Cannot release an Action which is not in a completed state.",
            )
        res = await async_invoke(
            self.handlers["release"],
            status,
            action_status=status,
            action_id=action_id,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        res = fill_action_status(res, req, auth_state)
        if self.persistence_backend is not None and status is not None:
            await self.persistence_backend.remove_action(action_id)
        return res

    async def cancel_handler(
        self,
        action_id: str,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        status, req, extra_data = await self.lookup_status(action_id)
        authorize_action_management(status, auth_state)
        if status is not None and status.is_complete():
            return status
        res = await async_invoke(
            self.handlers["cancel"],
            status,
            action_status=status,
            action_id=action_id,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        res = fill_action_status(res, req, auth_state)
        if self.persistence_backend is not None and status is not None:
            await self.persistence_backend.store_action(
                status, req, auth_state.effective_identity, extra_data
            )
        return res

    async def log_handler(
        self,
        action_id: str,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        status, req, extra_data = await self.lookup_status(action_id)
        authorize_action_access(status, auth_state)
        # TODO TODO: This is really all wrong as log is totally different
        # TODO: Check if it is already complete so we don't need to invoke the handler
        res = await async_invoke(
            self.handlers["log"],
            status,
            action_status=status,
            action_id=action_id,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        # TODO: Store the returned state in the backend
        return res

    async def resume_handler(
        self,
        action_id: str,
        auth_state: AuthState,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
    ) -> ActionStatus:
        status, req, extra_data = await self.lookup_status(action_id)
        authorize_action_management(status, auth_state)
        if status is not None and status.is_complete():
            return status
        res = await async_invoke(
            self.handlers["resume"],
            status,
            action_status=status,
            action_id=action_id,
            action_request=req,
            auth_state=auth_state,
            fastapi_request=request,
            fastapi_response=response,
            extra_data=extra_data,
            background_tasks=background_tasks,
        )
        res = fill_action_status(res, req, auth_state)
        if self.persistence_backend is not None and status is not None:
            await self.persistence_backend.store_action(
                status, req, auth_state.effective_identity, extra_data
            )
        return res

    def run(
        self, f: Callable[[ActionRequest], Union[ActionStatus, Awaitable[ActionStatus]]]
    ) -> Callable[[ActionRequest], ActionStatus]:
        self.handlers["run"] = f
        return f

    def status(self, f: StatusInOutCallable) -> Callable:
        self.handlers["status"] = f
        return f

    def resume(self, f: StatusInOutCallable) -> Callable:
        self.handlers["resume"] = f
        return f

    def cancel(self, f: StatusInOutCallable) -> Callable:
        self.handlers["cancel"] = f
        return f

    def release(self, f: StatusInOutCallable) -> Callable:
        self.handlers["release"] = f
        return f

    def log(self, f: StatusInOutCallable) -> Callable:
        self.handlers["log"] = f
        return f
