import json

from tests.conftest import api_event


def test_create_user(infra):
    import os

    print("PYTHONPATH", os.environ.get("PYTHONPATH"))
    from core.tables import AppTable
    from functions.rest import main as api

    response = api.handler(
        *api_event(
            "POST",
            "/users",
            body={"name": "Pytest User"},
        )
    )

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) is not None

    assert AppTable.Entities.User.model_validate_json(response["body"])
    return


# def test_get_layers(infra, seed_layers):
#     from core.tables import LayersTable
#     from rest.app import main as api

#     # Get all layers
#     response = api.handler(*api_event("GET", "/layers"))

#     assert response["statusCode"] == 200
#     assert json.loads(response["body"]) is not None

#     body = json.loads(response["body"])
#     assert len(body) == 144

#     for layer in body:
#         assert LayersTable.Entities.Layer.model_validate(layer)

#     # Get layers that match query
#     query = {
#         "provider": "Telstra",
#         "technology": "4G",
#         "metric": "BestServer",
#         # "height": "1.6",
#         "resolution": 20,
#         "version": 11111111,
#     }
#     response = api.handler(
#         *api_event(
#             "GET",
#             "/layers",
#             query=query,
#         )
#     )

#     assert response["statusCode"] == 200

#     for k, v in query.items():
#         assert json.loads(response["body"])[0][k] == v
