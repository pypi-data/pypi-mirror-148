from typing import Any, Dict, Optional, Tuple

from globus_action_provider_tools import ActionRequest, ActionStatus

from .fastapi_action_provider import (
    ActionProviderPersistence,
    ActionProviderPersistenceReturnType,
)


class InMemoryActionProviderPersistence(ActionProviderPersistence):
    def __init__(self):
        self.action_store: Dict[str, ActionProviderPersistenceReturnType] = {}
        self.by_request_id_index: Dict[Tuple[str, str], str] = {}

    async def lookup_by_action_id(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        return self.action_store.get(action_id, (None, None, None))

    async def lookup_by_request_id_and_identity(
        self, request_id: str, user_identity: str
    ) -> ActionProviderPersistenceReturnType:
        action_id = self.by_request_id_index.get((request_id, user_identity))
        if action_id is not None:
            return await self.lookup_by_action_id(action_id)
        else:
            return (None, None, None)

    async def store_action(
        self,
        action: ActionStatus,
        request: Optional[ActionRequest] = None,
        creator_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> ActionProviderPersistenceReturnType:
        self.action_store[action.action_id] = (action, request, extra_data)
        if request is not None and creator_id is not None:
            self.by_request_id_index[
                (request.request_id, creator_id)
            ] = action.action_id
        return action, request, extra_data

    async def remove_action(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        action, request, extra_data = await self.lookup_by_action_id(action_id)
        if action is not None:
            self.action_store.pop(action_id, None)
            if request is not None:
                self.by_request_id_index.pop(
                    (request.request_id, action.creator_id), None
                )
        return action, request, extra_data
