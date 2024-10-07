from core.controllers import UserController


def test_get_users():
    users = UserController.get_users()

    assert len(users) == 10, "Wrong number of users"
