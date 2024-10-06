import json

from core.controllers import UserController


def handler(event, context):
    users = UserController.get_users()
    print(users)
    return {"statusCode": 200, "body": json.dumps(users)}
