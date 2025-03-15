import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import Client, create_client
from functools import wraps

from happybarra.models import CreditCardInstance

logging.basicConfig(level=logging.DEBUG)

_logger = logging.getLogger(__name__)


app = FastAPI()

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def logged(func, logger: logging.Logger = None):
    logger = _logger or logger

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(
            "Executing %s with the following arguments: {'args'='%s', 'kwargs'='%s'",
            func.__name__,
            args,
            kwargs,
        )
        result = func(*args, **kwargs)
        logger.debug("%s execution done", func.__name__)
        return result

    return wrapper


@logged
def get_bank(name: str = ""):
    response = supabase.table("bank").select("*").eq("alias", name).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items."
        else:
            msg = "Database did not return anything."
        _logger.error(msg)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]


@logged
def get_network(name: str = ""):
    response = supabase.table("network").select("*").eq("name", name).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items."
        else:
            msg = "Database did not return anything."
        _logger.error(msg)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]


@logged
def get_credit_card(name: str = "", bank: str = "", network: str = "") -> dict:
    """
    Something something
    """
    bank_response = get_bank(bank)
    bank_name = bank_response["name"]
    bank_id = bank_response["id"]
    bank_alias = bank_response["alias"]

    network_response = get_network(network)
    network_name = network_response["name"]
    network_id = network_response["id"]

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
            msg = "Error: database returned multiple items."
        else:
            msg = "Database did not return anything."
        _logger.error(msg)
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


@logged
def post_credit_card_instance(
    credit_card_instance_request: CreditCardInstanceCreationModel,
):

    credit_card_response = get_credit_card(
        name=credit_card_instance_request.credit_card,
        bank=credit_card_instance_request.bank,
        network=credit_card_instance_request.network,
    )
    credit_card_id = credit_card_response["id"]

    response = (
        supabase.table("credit_card_instance")
        .insert(
            {
                "name": credit_card_instance_request.name,
                "credit_card_id": credit_card_id,
                "statement_day": credit_card_instance_request.statement_day,
                "due_date_reference": credit_card_instance_request.statement_day,
            }
        )
        .execute()
    )
    return dict(response)


@app.post("/api/v1/create_credit_card")
async def api_post_credit_card_instance(
    credit_card_instance_request: CreditCardInstanceCreationModel,
):
    return post_credit_card_instance(
        credit_card_instance_request=credit_card_instance_request
    )
