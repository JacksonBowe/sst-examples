from typing import List


def get_users() -> List[dict]:
    # Fetch users from your database of choice

    # Dummy code
    users = []
    for i in 10:
        users.append({"id": f"user={1}", "name": f"User{i}"})

    return users
