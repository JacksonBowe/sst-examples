from core import hello


def handler(event, context):
    hello()
    print("Hello from API")

    return {"statusCode": 200, "body": "Hello from API!"}
