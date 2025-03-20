import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import Client, create_client

from happybarra.utils import logged

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


app = FastAPI()

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)


@logged(logger=_logger)
def get_bank(name: str = ""):
    response = supabase.table("bank").select("*").eq("alias", name).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items. \n%s"
        else:
            msg = "Database did not return anything. \n%s"
        _logger.error(msg % assert_error)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]


@logged(logger=_logger)
def get_network(name: str = ""):
    response = supabase.table("network").select("*").eq("name", name).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items. \n %s"
        else:
            msg = "Database did not return anything. \n %s"
        _logger.error(msg % assert_error)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]


@logged(logger=_logger)
def get_credit_card(name: str = "", bank: str = "", network: str = "") -> dict:
    """
    Something something
    """
    bank_response = get_bank(bank)
    bank_id = bank_response["id"]
    _logger.debug("bank_response: %s", bank_response)

    network_response = get_network(network)
    network_id = network_response["id"]
    _logger.debug("network_response: %s", network_response)

    try:
        response = (
            supabase.table("credit_card")
            .select("*")
            .eq("bank_id", bank_id)
            .eq("network_id", network_id)
            .eq("name", name)
            .execute()
        )
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items. \n%s"
        else:
            msg = "Database did not return anything. \n%s"
        _logger.error(msg % assert_error)
        raise AssertionError(msg)
    return dict(response)["data"][0]


@app.get("/api/v1/health/")
async def health():
    return {"status": "happybarra is healthy 💖"}


@app.get("/api/v1/bank/")
async def api_get_bank(name: str = ""):
    return get_bank(name)


@app.get("/api/v1/network/")
async def api_get_network(name: str = ""):
    return get_network(name)


@app.get("/api/v1/credit_card/")
async def api_get_credit_card(name: str = "", bank: str = "", network: str = ""):
    return get_credit_card(name=name, bank=bank, network=network)


class CreditCardInstanceCreationModel(BaseModel):
    name: str
    bank: str
    network: str
    credit_card: str
    statement_day: int
    due_date_reference: int


@logged(logger=_logger)
def post_credit_card_instance(
    credit_card_instance_request: CreditCardInstanceCreationModel,
):
    credit_card_response = get_credit_card(
        name=credit_card_instance_request.credit_card,
        bank=credit_card_instance_request.bank,
        network=credit_card_instance_request.network,
    )
    credit_card_id = credit_card_response["id"]

    user_id = supabase.auth.get_user().model_dump()["user"]["id"]
    response = (
        supabase.table("credit_card_instance")
        .insert(
            {
                "name": credit_card_instance_request.name,
                "credit_card_id": credit_card_id,
                "statement_day": credit_card_instance_request.statement_day,
                "due_date_reference": credit_card_instance_request.statement_day,
                "user_id": user_id,
                # for quick development, use this
                # "user_id": "4b69e475-9202-47f0-a853-a9c92428b2eb",
            }
        )
        .execute()
    )
    return response.model_dump()


@app.post("/api/v1/create_credit_card")
async def api_post_credit_card_instance(
    request_body: dict,
):
    _logger.debug("cci_request: %s", request_body)
    modeled_request = CreditCardInstanceCreationModel(**request_body)
    return post_credit_card_instance(credit_card_instance_request=modeled_request)


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


@logged(logger=_logger)
def post_login(login_request: LoginRequest):
    response = supabase.auth.sign_in_with_password(
        {
            "email": login_request.email,
            "password": login_request.password,
        }
    )
    login_response = LoginResponse(
        access_token=dict(dict(response)["session"])["access_token"],
        refresh_token=dict(dict(response)["session"])["refresh_token"],
    )
    return login_response


@app.post("/api/v1/login")
async def api_post_login(login_request: LoginRequest) -> LoginResponse:
    return post_login(login_request)


class LogoutRequest(BaseModel): ...


class LogoutResponse(BaseModel):
    msg: str


@logged(logger=_logger)
def post_logout() -> LogoutResponse:
    supabase.auth.sign_out()
    return LogoutResponse(msg="success")


@app.post("/api/v1/logout")
async def api_post_logout() -> LogoutResponse:
    return post_logout()
