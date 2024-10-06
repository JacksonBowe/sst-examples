from core import hello

from core import sum
from core.test.hello import test_hello

print("HHHHHHHHHHHHHHHHHHHHHHHH")


def handler(event, context):
    print("Hello from function")
    test_hello()
    return
