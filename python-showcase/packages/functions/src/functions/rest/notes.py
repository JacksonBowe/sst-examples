import os
from typing import List

from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter
from aws_lambda_powertools.utilities.parser import BaseModel
from core.controllers import NoteController
from core.tables import AppTable

os.environ["POWERTOOLS_SERVICE_NAME"] = "notes"
router = APIGatewayHttpRouter()


class CreateUserNotePayload(BaseModel):
    content: str


# NOTE: If Users are creating their own notes you would need to ensure that
# there are safeguards in place to prevent them creating notes for other users.

# Typically you'd require an AccessToken with each request, and you can pull the user_id
# from that AccessToken. I'm taking a shortcut here just for an example


@router.post("/users/<user_id>/notes")
def create_user(
    user_id: str, payload: CreateUserNotePayload
) -> AppTable.Entities.UserNote:
    return NoteController.create_user_note(user_id, **payload.model_dump())


@router.get("/users/<user_id>/notes")
def get_users(user_id: str) -> List[AppTable.Entities.UserNote]:
    return NoteController.get_user_notes(user_id)
