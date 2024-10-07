import uuid
from typing import List

import boto3
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
)
from aws_lambda_powertools.utilities.parser import BaseModel
from aws_lambda_powertools.logging import Logger
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from core.tables import AppTable
from core.events import Event

ddb = boto3.resource("dynamodb")
logger = Logger()


class Events:
    class NoteCreated(Event):
        event_name = "note.created"

        class Properties(BaseModel):
            user_id: str
            timestamp: str


def create_user_note(user_id: str, content: str) -> AppTable.Entities.UserNote:
    user_note = AppTable.Entities.UserNote(
        entityId=str(uuid.uuid4()), user_id=user_id, content=content
    )

    try:
        AppTable.table.put_item(Item=user_note.serialize())
    except ClientError as e:
        logger.error(
            f"Error writing new user to dynamo: {e.response['Error']['Message']}"
        )
        raise InternalServerError(
            f"Error putting item: {e.response['Error']['Message']}"
        )

    # Send an event to the Event Bus
    Events.NoteCreated.publish({"user_id": user_id, "timestamp": "some timestamp"})

    return user_note


def get_user_notes(user_id: str) -> List[AppTable.Entities.UserNote]:
    try:
        # Querying with entityType as hash key and PK as sort key
        items = AppTable.table.query(
            IndexName=AppTable.Indexes.ITEMS_BY_TYPE.value,
            KeyConditionExpression=Key("entityType").eq(
                AppTable.EntityTypes.USER_NOTE.value
            )
            & Key("PK").eq(user_id),
        ).get("Items", [])
    except ClientError as e:
        logger.error(f"Error querying user notes: {e.response['Error']['Message']}")
        raise InternalServerError(
            f"Error querying user notes: {e.response['Error']['Message']}"
        )

    return [AppTable.Entities.UserNote.deserialize(item) for item in items]
