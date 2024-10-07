from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent, event_source
from core.controllers import NoteController


@event_source(data_class=EventBridgeEvent)
def handler(event: EventBridgeEvent, context):
    details = NoteController.Events.NoteCreated.Properties(**event.detail)

    print(f"Note created at {details.timestamp} for user {details.user_id}")

    return
