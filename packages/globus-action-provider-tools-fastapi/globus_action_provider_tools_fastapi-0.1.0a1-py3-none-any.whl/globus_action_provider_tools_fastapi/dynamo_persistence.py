import json
import logging
from typing import Any, Dict, Optional, Type, TypeVar

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError, EndpointConnectionError
from globus_action_provider_tools import (
    ActionProviderJsonEncoder,
    ActionRequest,
    ActionStatus,
    ActionStatusValue,
)
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table as DynamoTable
from pydantic import BaseModel

from .fastapi_action_provider import (
    ActionProviderPersistence,
    ActionProviderPersistenceReturnType,
)

log = logging.getLogger(__name__)

_attribute_definitions = ({"AttributeName": "action_id", "AttributeType": "S"},)

_key_schema = ({"AttributeName": "action_id", "KeyType": "HASH"},)

T = TypeVar("T", bound=BaseModel)

_action_property_conversions = {
    "status": lambda x: ActionStatusValue[x],
}


def create_dynamo_client(**kwargs) -> DynamoDBServiceResource:
    client = boto3.resource("dynamodb", **kwargs)
    return client


def _json_to_object(json_val: Optional[str], model_class: Type[T]) -> Optional[T]:
    if json_val is None:
        return None
    props = json.loads(json_val)
    for val_to_convert, convert_fn in _action_property_conversions.items():
        dynamo_val = props.get(val_to_convert)
        if dynamo_val is not None:
            props[val_to_convert] = convert_fn(dynamo_val)
    return model_class(**props)


def _dynamo_item_to_return_vals(
    item: Optional[Dict[str, Any]]
) -> ActionProviderPersistenceReturnType:
    if item is None:
        return None, None, None
    action_status = _json_to_object(item.get("action_status"), ActionStatus)
    request = _json_to_object(item.get("action_request"), ActionRequest)
    extra_data = item.get("extra_data")
    return action_status, request, extra_data


class DynamoActionProviderPersistence(ActionProviderPersistence):
    def __init__(
        self,
        dynamo_client: DynamoDBServiceResource,
        table_name: str,
        create_table=False,
        create_table_args: Optional[Dict] = None,
    ):
        self.client = dynamo_client
        self.table_name = table_name
        if create_table:
            if create_table_args is None:
                create_table_args = {}
            self.table = self.create_table(self.table_name, **create_table_args)
        else:
            self.table = self.client.Table(table_name)

    def create_table(self, table_name: Optional[str] = None, **kwargs) -> DynamoTable:
        if table_name is None:
            table_name = self.table_name
        try:
            self.client.create_table(
                TableName=table_name,
                AttributeDefinitions=_attribute_definitions,
                KeySchema=_key_schema,
                **kwargs,
            )
        except ClientError as ce:
            if ce.response["Error"]["Code"] == "ResourceInUseException":
                log.info(f"Dynamo table {table_name} already exists.")
            else:
                log.info(f"Error creating dynamo table {table_name}: {ce}")
        except EndpointConnectionError as err:
            log.info(f"Error creating dynamo table {table_name}: {err}")

        return self.client.Table(table_name)

    async def lookup_by_action_id(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        response = self.table.query(
            KeyConditionExpression=Key("action_id").eq(action_id)
        )
        items = response.get("Items")

        if items is None:
            item = None
        elif len(items) == 0:
            item = None
        else:
            item = items[0]
        return _dynamo_item_to_return_vals(item)

    async def lookup_by_request_id_and_identity(
        self, request_id: str, user_identity: str
    ) -> ActionProviderPersistenceReturnType:
        filter_expression = Attr("request_id").eq(request_id) & Attr("creator").eq(
            user_identity
        )
        response = self.table.scan(FilterExpression=filter_expression)
        items = response.get("Items", (None,))
        if len(items) == 0:
            items = (None,)
        return _dynamo_item_to_return_vals(items[0])

    async def store_action(
        self,
        action: ActionStatus,
        request: Optional[ActionRequest] = None,
        creator_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> ActionProviderPersistenceReturnType:
        action_json = json.dumps(action, cls=ActionProviderJsonEncoder)

        item = {
            "action_id": action.action_id,
            "creator": action.creator_id,
            "action_status": action_json,
        }
        if request is not None:
            request_json = json.dumps(request, cls=ActionProviderJsonEncoder)
            item["request_id"] = request.request_id
            item["action_request"] = request_json
        if extra_data is not None:
            item["extra_data"] = extra_data

        self.table.put_item(Item=item)
        return action, request, extra_data

    async def remove_action(
        self, action_id: str
    ) -> ActionProviderPersistenceReturnType:
        del_resp = self.table.delete_item(
            Key={
                "action_id": action_id,
            },
            ReturnValues="ALL_OLD",
        )
        item = del_resp.get("Attributes")
        # Make it an iterable to pass in there
        return _dynamo_item_to_return_vals(item)
