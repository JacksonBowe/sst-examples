import os
import sys

if os.getenv("IS_LOCAL"):  # In local dev add packages/ to path
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

from core import modA

def handler(event, context):
    print(modA.mod_a_test_func())
    return {"statusCode": 200, "body": "Hello, World!"}
