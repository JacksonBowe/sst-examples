import json
import os
from dataclasses import dataclass

import boto3
import pytest

from moto import mock_aws


# Provision mock infrastructure
@pytest.fixture(scope="function")
def environment():
    """Mocked Environment Variables for moto."""
    # AWS
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"
    os.environ["AWS_REGION"] = "ap-southeast-2"

    # SST
    os.environ["SST_APP"] = "python-showcase-test"
    os.environ["SST_STAGE"] = "test"
    os.environ["IS_LOCAL"] = "true"

    # PYTEST
    os.environ["PYTEST"] = "true"


@pytest.fixture(scope="function")
def aws(environment):
    with mock_aws():
        yield


# --- APP INFRASTRUCTURE --- #
@pytest.fixture
def storage_app_table(aws):
    # Create the table
    ddb = boto3.resource("dynamodb")
    table = ddb.create_table(
        TableName="AppTable",
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "entityType", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "itemsByType",
                "KeySchema": [
                    {"AttributeName": "entityType", "KeyType": "HASH"},
                    {"AttributeName": "PK", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    # Ensure the table is active
    table.meta.client.get_waiter("table_exists").wait(TableName="AppTable")

    # Set the environment variable
    os.environ["SST_TABLE_TABLENAME_APPTABLE"] = table.table_name

    return table


@pytest.fixture
def infra(storage_app_table):
    return


def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = (
            "arn:aws:lambda:eu-west-1:123456789012:function:test"
        )
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return LambdaContext()


def api_event(method, route, query: dict = None, body: dict = None):
    return {
        "rawPath": route,
        "requestContext": {
            "http": {
                "method": method,
            },
            "stage": "$default",
        },
        "queryStringParameters": query,
        "body": json.dumps(body),
    }, lambda_context()
