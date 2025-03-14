import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import Client, create_client

from happybarra.models import CreditCardInstance

_logger = logging.getLogger(__name__)
logging.basicConfig()

app = FastAPI()

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_bank(name: str = ""):
    response = (
        supabase.table("bank")
        .select("*")
        .eq("alias", name)
        .execute()
    )

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items."
        else:
            msg = "Database did not return anything."
        _logger.error(msg)
    finally:
        response = response or {"Error": msg}

    # return the row
    return dict(response)

def get_network(name: str = ""):
    response = (
        supabase.table("network")
        .select("*")
        .eq("name", name)
        .execute()
    )

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items."
        else:
            msg = "Database did not return anything."
        _logger.error(msg)
    finally:
        response = response or {"Error": msg}

    # return the row
    return dict(response)

@app.get("/api/v1/health/")
async def health():
    return {"status": "happybarra is healthy 💖"}

@app.post("/api/v1/create_credit_card_instance")
async def create_credit_card_instance(credit_card_instance: CreditCardInstance):

    # validate that the bank and network exists in the database
    assert "Error" not in get_bank(credit_card_instance.credit_card.bank.name)
    assert "Error" not in get_network(credit_card_instance.credit_card.network.name)
    return credit_card_instance

@app.get("/api/v1/bank/")
async def api_get_bank(name: str = ""):
    return get_bank(name)

@app.get("/api/v1/network/")
async def api_get_network(name: str = ""):
    return get_network(name)
    





