import os
from typing import List, Literal, Optional

from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.utilities.parser import BaseModel, Field

from core.controllers import UserController

os.environ["POWERTOOLS_SERVICE_NAME"] = "users"
router = APIGatewayHttpRouter()

# @router.post("/users")


@router.get("/users")
def get_users() -> List[dict]:
    return UserController.get_users()
