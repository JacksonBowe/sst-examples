from __future__ import annotations

import os
from enum import Enum

import boto3
from core.utils.dynamo import CompositeEntity

table_name = os.environ.get("SST_TABLE_TABLENAME_APPTABLE")
if table_name:
    ddb = boto3.resource("dynamodb")
    table = ddb.Table(table_name)


class Indexes(Enum):
    ITEMS_BY_TYPE = "itemsByType"


class EntityTypes(Enum):
    USER = "USER"
    USER_NOTE = "USER_NOTE"


class Entities:
    class BaseEntity(CompositeEntity):
        entityId: str
        entityType: EntityTypes

    class User(BaseEntity):
        entityType: EntityTypes = EntityTypes.USER
        name: str

        @property
        def PK(self):
            return self.entityId

        @property
        def SK(self):
            return "A"

    class UserNote(BaseEntity):
        entityType: EntityTypes = EntityTypes.USER_NOTE
        user_id: str
        content: str

        @property
        def PK(self):
            """The USER_NOTE entity is contained by the USER entity"""
            return self.user_id

        @property
        def SK(self):
            return self.entityId
