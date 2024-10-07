import os
from typing import List

from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.utilities.parser import BaseModel
from core.controllers import UserController
from core.tables import AppTable

os.environ["POWERTOOLS_SERVICE_NAME"] = "users"
router = APIGatewayHttpRouter()


class CreateUserPayload(BaseModel):
    name: str


@router.post("/users")
def create_user(payload: CreateUserPayload) -> AppTable.Entities.User:
    return UserController.create_user(**payload.model_dump())


@router.get("/users")
def get_users() -> List[AppTable.Entities.User]:
    return UserController.get_users()
