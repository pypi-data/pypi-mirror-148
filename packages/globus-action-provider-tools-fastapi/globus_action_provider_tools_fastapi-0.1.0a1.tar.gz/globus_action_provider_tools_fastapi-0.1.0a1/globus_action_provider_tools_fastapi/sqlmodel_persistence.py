import datetime
import json
import logging
from typing import Any, Dict, Optional, Set, Type, TypeVar

from globus_action_provider_tools import (
    ActionProviderJsonEncoder,
    ActionRequest,
    ActionStatus,
    ActionStatusValue,
)
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .fastapi_action_provider import (
    ActionProviderPersistence,
    ActionProviderPersistenceReturnType,
)

log = logging.getLogger(__name__)

_action_property_conversions = {
    "status": lambda x: ActionStatusValue[x],
}

T = TypeVar("T", bound=BaseModel)


def _copy_into(
    src_model: BaseModel, dest_model: BaseModel, omits: Optional[Set[str]] = None
) -> BaseModel:
    for k, v in src_model:
        if omits and k not in omits:
            setattr(dest_model, k, v)
    return dest_model


def _json_to_object(json_val: Optional[str], model_class: Type[T]) -> Optional[T]:
    if json_val is None:
        return None
    props = json.loads(json_val)
    for val_to_convert, convert_fn in _action_property_conversions.items():
        model_val = props.get(val_to_convert)
        if model_val is not None:
            props[val_to_convert] = convert_fn(model_val)
    return model_class(**props)


class ActionTableModel(SQLModel, table=True):
    __tablename__ = "GlobusActions"
    action_id: str = Field(primary_key=True)
    request_id: str = Field(index=True)
    creator: str = Field(index=True)
    completion_time: Optional[datetime.datetime]
    action_status_json: str
    request_json: Optional[str]
    extra_data_json: Optional[str]

    def to_persistence_return_type(self) -> ActionProviderPersistenceReturnType:
        action_status = _json_to_object(self.action_status_json, ActionStatus)
        request = _json_to_object(self.request_json, ActionRequest)
        extra_data = _json_to_object(self.extra_data_json, dict)
        return (action_status, request, extra_data)


class SQLModelProviderPersistence(ActionProviderPersistence):
    def __init__(
        self,
        engine: Optional = None,
        db_url: Optional[str] = None,
        create_tables=False,
        create_engine_args: Optional[Dict] = None,
    ):
        if engine is None and db_url is None:
            raise ValueError("At least one of engine or db_url must be provided")
        if engine is None and db_url is not None:
            if create_engine_args is None:
                create_engine_args = {}
            engine = self.create_engine(db_url, **create_engine_args)
        self.engine = engine
        if create_tables:
            self.create_tables()

    def create_engine(self, db_url: str, **kwargs):
        return create_engine(db_url, **kwargs)

    def create_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_session(self, **kwargs) -> Session:
        return Session(self.engine, **kwargs)

    async def lookup_by_action_id(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        with self.get_session(expire_on_commit=False) as session:
            table_model = session.get(ActionTableModel, action_id)
            if table_model is None:
                return (None, None, None)
            else:
                return table_model.to_persistence_return_type()

    async def lookup_by_request_id_and_identity(
        self, request_id: str, user_identity: str
    ) -> ActionProviderPersistenceReturnType:
        with self.get_session(expire_on_commit=False) as session:
            table_model = session.exec(
                select(ActionTableModel).where(
                    ActionTableModel.request_id == request_id
                    and ActionTableModel.creator == user_identity
                )
            ).first()
            if table_model is None:
                return (None, None, None)
            else:
                return table_model.to_persistence_return_type()

    async def store_action(
        self,
        action: ActionStatus,
        request: Optional[ActionRequest] = None,
        creator_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> ActionProviderPersistenceReturnType:
        action_json = json.dumps(action, cls=ActionProviderJsonEncoder)

        if request is not None:
            request_json = json.dumps(request, cls=ActionProviderJsonEncoder)
            request_id = request.request_id
        else:
            request_json = None
            request_id = None
        if extra_data is not None:
            extra_data_json = json.dumps(extra_data, cls=ActionProviderJsonEncoder)
        else:
            extra_data_json = None

        table_model = ActionTableModel(
            action_id=action.action_id,
            action_status_json=action_json,
            request_id=request_id,
            request_json=request_json,
            creator=creator_id,
            completion_time=action.completion_time,
            extra_data_json=extra_data_json,
        )

        rvals: ActionProviderPersistenceReturnType = (None, None, None)
        with self.get_session() as session:
            current_entry = session.get(ActionTableModel, action.action_id)
            if current_entry is not None:
                # The action, the completion time, and the extra data are the
                # only mutable fields
                current_entry.action_status_json = action_json
                current_entry.completion_time = action.completion_time
                current_entry.extra_data_json = extra_data_json
                session.add(current_entry)
                rvals = current_entry.to_persistence_return_type()
            else:
                session.add(table_model)
                rvals = table_model.to_persistence_return_type()
            session.commit()
        return rvals

    async def remove_action(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        with self.get_session(expire_on_commit=False) as session:
            table_model = session.get(ActionTableModel, action_id)
            if table_model is not None:
                session.delete(table_model)
                session.commit()
                return table_model.to_persistence_return_type()
            else:
                return (None, None, None)
