import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from happybarra.backend.dependencies import (
    Client,
    apikey_scheme,
    get_authed_supabase_client,
    oauth2_scheme,
    rcv_acc_token,
    supabase,
)
from happybarra.backend.services.helpers import async_logged

#
# Create logger
_logger = logging.getLogger("happybarra.backend.routers.credit_cards")

router = APIRouter(prefix="/api/v1/credit_cards", tags=["Credit Cards"])


class User(BaseModel):
    id: str
    email: str


async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return User(id="eme")


class CreditCardInstanceMapModel(BaseModel):
    credit_card_instance__id: str
    credit_card_instance__name: str
    credit_card__name: str
    bank__name: str
    network__name: str
    credit_card_instance__due_date_reference: int
    credit_card_instance__statement_day: int
    credit_card_instance__user_id: str
    credit_card__id: str
    bank__id: str
    network__id: str


class CreditCards(BaseModel):
    data: List[CreditCardInstanceMapModel]


@async_logged(_logger)
@router.get("/credit_cards")
async def yoink_credit_cards_by_user(
    authed_supabase_client: Annotated[Client, Depends(get_authed_supabase_client)],
):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    response = (
        authed_supabase_client.table("credit_card_instance_map").select("*").execute()
    )

    return CreditCards(**response.model_dump())


@async_logged(_logger)
@router.get("/credit_cards_fast")
async def yoink_fast():
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    access_token = "--.--.--"
    request = supabase().table("credit_card_instance_map").select("*")
    request.headers = {
        "Authorization": f"Bearer {access_token}"
    } or request.headers.update({"Authorization": f"Bearer {access_token}"})
    response = request.execute()
    return CreditCards(**response.model_dump())


@async_logged(_logger)
@router.get("/credit_cards_fasther")
async def yoink_fasther(auth_dict: Annotated[dict, Depends(rcv_acc_token)]):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    request = supabase().table("credit_card_instance_map").select("*")
    request.headers = auth_dict or request.headers.update(auth_dict)
    response = request.execute()
    return CreditCards(**response.model_dump())


@async_logged(_logger)
@router.get("/credit_cards_fastherest")
async def yoink_fastherest(authorization: str = Depends(apikey_scheme)):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    if not authorization:
        HTTPException(status_code=401, detail="No doba doba provided. Mirku sadge.")
    if "Bearer " not in authorization:
        raise HTTPException(
            status_code=401, detail="doba doba seems dysfunctional. Mirku Sadge"
        )

    request = supabase().table("credit_card_instance_map").select("*")
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)
    response = request.execute()
    return CreditCards(**response.model_dump())
