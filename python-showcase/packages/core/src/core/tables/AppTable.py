from __future__ import annotations

import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Literal, Optional, Self

import boto3

table_name = os.environ.get("SST_TABLE_TABLENAME_APPTABLE")
if table_name:
    ddb = boto3.resource("dynamodb")
    table = ddb.Table(table_name)


class Indexes:
    pass


class EntityTypes(Enum):
    USER = "USER"
    USER_NOTE = "USER_NOTE"
