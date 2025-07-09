import logging
import os

import yaml
from fastapi import FastAPI

from .routers import banks, credit_cards, dues, security, savings

tags_metadata = [
    {
        "name": "Banks",
        "description": "Bank operations my guy",
    },
    {"name": "Security", "description": "PM is the 🔒"},
    {"name": "Credit Cards", "description": "well, stuff we want (or not) to track"},
    {"name": "Dues", "description": "stay on top"},
    {"name": "Savings", "description": "probably non-existent 😉"},
]


def setup_logging():
    # Let's setup the logging

    # Figure out the pathing for the log config
    script_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(script_path)
    config_path = os.path.join(dir_name, "debug_logging_conf.yaml")

    # Then load the config yaml to setup the logging
    with open(config_path, "rt") as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config=config)

    # Now let's get a logger for this module.
    _logger = logging.getLogger("happybarra")
    _logger.info("🐹 initialized")
    # Logger setup done.


setup_logging()

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(banks.router)
app.include_router(security.router)
app.include_router(credit_cards.router)
app.include_router(dues.router)
app.include_router(savings.router)


@app.get("/")
async def health():
    return {"status": "happybarra is healthy 💖"}


# @logged(_logger)
# def get_network(name: str = ""):
#     response = supabase.table("network").select("*").eq("name", name).execute()
#     _logger.debug(response)

#     # validation: ensure that the query returned only one row
#     try:
#         assert len(dict(response)["data"]) == 1
#     except AssertionError as assert_error:
#         if len(dict(response)["data"]) > 1:
#             msg = "Error: database returned multiple items. \n %s"
#         else:
#             msg = "Database did not return anything. \n %s"
#         _logger.error(msg % assert_error)
#         raise AssertionError(msg)

#     # return the row
#     return dict(response)["data"][0]


# @logged(_logger)
# def get_credit_card(name: str = "", bank: str = "", network: str = "") -> dict:
#     """
#     Something something
#     """
#     bank_response = get_bank(bank)
#     bank_id = bank_response["id"]
#     _logger.debug("bank_response: %s", bank_response)

#     network_response = get_network(network)
#     network_id = network_response["id"]
#     _logger.debug("network_response: %s", network_response)

#     try:
#         response = (
#             supabase.table("credit_card")
#             .select("*")
#             .eq("bank_id", bank_id)
#             .eq("network_id", network_id)
#             .eq("name", name)
#             .execute()
#         )
#         assert len(dict(response)["data"]) == 1
#     except AssertionError as assert_error:
#         if len(dict(response)["data"]) > 1:
#             msg = "Error: database returned multiple items. \n%s"
#         else:
#             msg = "Database did not return anything. \n%s"
#         _logger.error(msg % assert_error)
#         raise AssertionError(msg)
#     return dict(response)["data"][0]


# @app.get("/api/v1/network/")
# async def api_get_network(name: str = ""):
#     return get_network(name)


# @app.get("/api/v1/credit_card/")
# async def api_get_credit_card(name: str = "", bank: str = "", network: str = ""):
#     return get_credit_card(name=name, bank=bank, network=network)


# class CreditCardInstanceCreationModel(BaseModel):
#     name: str
#     bank: str
#     network: str
#     credit_card: str
#     statement_day: int
#     due_date_reference: int


# @logged(_logger)
# def post_credit_card_instance(
#     credit_card_instance_request: CreditCardInstanceCreationModel,
# ):
#     credit_card_response = get_credit_card(
#         name=credit_card_instance_request.credit_card,
#         bank=credit_card_instance_request.bank,
#         network=credit_card_instance_request.network,
#     )
#     credit_card_id = credit_card_response["id"]

#     user_id = supabase.auth.get_user().model_dump()["user"]["id"]
#     response = (
#         supabase.table("credit_card_instance")
#         .insert(
#             {
#                 "name": credit_card_instance_request.name,
#                 "credit_card_id": credit_card_id,
#                 "statement_day": credit_card_instance_request.statement_day,
#                 "due_date_reference": credit_card_instance_request.statement_day,
#                 "user_id": user_id,
#                 # for quick development, use this
#                 # "user_id": "4b69e475-9202-47f0-a853-a9c92428b2eb",
#             }
#         )
#         .execute()
#     )
#     return response.model_dump()


# @app.post("/api/v1/create_credit_card")
# async def api_post_credit_card_instance(
#     request_body: dict,
# ):
#     _logger.debug("cci_request: %s", request_body)
#     modeled_request = CreditCardInstanceCreationModel(**request_body)
#     return post_credit_card_instance(credit_card_instance_request=modeled_request)


# class LoginRequest(BaseModel):
#     email: str
#     password: str


# class LoginResponse(BaseModel):
#     access_token: str
#     refresh_token: str


# class LogoutRequest(BaseModel): ...


# class LogoutResponse(BaseModel):
#     msg: str


# @logged
# def post_logout() -> LogoutResponse:
#     supabase.auth.sign_out()
#     return LogoutResponse(msg="success")


# @app.post("/api/v1/logout")
# async def api_post_logout() -> LogoutResponse:
#     return post_logout()
