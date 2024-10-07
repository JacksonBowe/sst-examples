import uuid
from typing import List

import boto3
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
)
from aws_lambda_powertools.logging import Logger
from botocore.exceptions import ClientError

from core.tables import AppTable

ddb = boto3.resource("dynamodb")
logger = Logger()


def create_user(name: str) -> AppTable.Entities.User:
    user = AppTable.Entities.User(entityId=str(uuid.uuid4()), name=name)

    print(user.model_dump_json())
    try:
        AppTable.table.put_item(Item=user.serialize())
    except ClientError as e:
        logger.error(
            f"Error writing new user to dynamo: {e.response['Error']['Message']}"
        )
        raise InternalServerError(
            f"Error putting item: {e.response['Error']['Message']}"
        )

    return user


def get_users() -> List[AppTable.Entities.User]:
    try:
        items = AppTable.table.query(
            IndexName=AppTable.Indexes.ITEMS_BY_TYPE.value,
            KeyConditionExpression="#t = :t",
            ExpressionAttributeNames={"#t": "entityType"},
            ExpressionAttributeValues={":t": AppTable.EntityTypes.USER.value},
        ).get("Items", [])
    except ClientError as e:
        logger.error(f"Error querying items by type: {e.response['Error']['Message']}")
        raise InternalServerError(
            f"Error querying items by type: {e.response['Error']['Message']}"
        )

    return [AppTable.Entities.User.deserialize(item) for item in items]
