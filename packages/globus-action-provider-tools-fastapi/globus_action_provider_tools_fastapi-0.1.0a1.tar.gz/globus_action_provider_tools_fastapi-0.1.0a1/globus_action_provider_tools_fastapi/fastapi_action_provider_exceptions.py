from typing import Any, Dict, Optional

from fastapi.exceptions import HTTPException


class ActionProviderException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code, detail=detail, headers=headers)


class ActionNotFoundException(ActionProviderException):
    def __init__(self, action_id: str):
        super().__init__(
            status_code=404, detail=f"Action with id {action_id} not Found"
        )


class ActionConflictException(ActionProviderException):
    def __init__(self, action_id: str, detail: Optional[str]):
        super().__init__(status_code=409, detail=detail)


class ApplicationError(ActionProviderException):
    def __init__(self, detail: Optional[str]):
        super().__init__(status_code=500, detail=detail)


class ActionMethodMissingImplementation(ActionProviderException):
    def __init__(self, method_name: str):
        super().__init__(
            status_code=500,
            detail=f"Server failed to implement required method {method_name}",
        )


class UnauthorizedException(ActionProviderException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail=(
                "The server could not verify that you are authorized to access"
                " the URL requested. You either supplied the wrong credentials"
                " (e.g. a bad password), or your browser doesn't understand"
                " how to supply the credentials required."
            ),
        )
