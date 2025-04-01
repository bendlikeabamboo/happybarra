import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from happybarra.backend.dependencies import (
    Client,
    apikey_scheme,
    get_authed_supabase_client,
    oauth2_scheme,
    send_execute_commnad,
    supabase,
    verify_auth_header,
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
@router.get("/credit_cards_with_refresh")
async def yoink_credit_cards_by_user(
    authed_supabase_client: Annotated[Client, Depends(get_authed_supabase_client)],
):
    """
    ⚠️ FOR DEPRECATION | Retrieve credit card instances that belong to the logged-in
    user
    """
    response = (
        authed_supabase_client.table("credit_card_instance_map").select("*").execute()
    )

    return CreditCards(**response.model_dump())


@async_logged(_logger)
@router.get("/credit_cards")
async def yoink_credit_cards(authorization: str = Depends(apikey_scheme)):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    verify_auth_header(authorization=authorization)

    request = supabase().table("credit_card_instance_map").select("*")

    # build the headers for the request then update the header
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)

    # execute the command
    response = send_execute_commnad(request=request)

    # return the dataclass
    return CreditCards(**response.model_dump())


class CreditCardStatementDayUpdate(BaseModel):
    id: str
    statement_day: str


@async_logged(_logger)
@router.post("/update_credit_card_statement_date")
async def update_credit_card_statement_date(
    modified_credit_card_instance: CreditCardStatementDayUpdate,
    authorization: str = Depends(apikey_scheme),
):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    verify_auth_header(authorization=authorization)

    _logger.debug("Instance to be modified: %s", modified_credit_card_instance)
    # prepare the request
    request = (
        supabase()
        .table("credit_card_instance")
        .update(modified_credit_card_instance.model_dump())
        .eq("id", modified_credit_card_instance.id)
    )

    # build the headers for the request then update the header
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)

    _logger.debug("Sending update command")
    # execute the command
    response = send_execute_commnad(request=request)

    # return the dataclass
    return response.model_dump()


class CreditCardDueDateReferenceUpdate(BaseModel):
    id: str
    due_date_reference: int


@async_logged(_logger)
@router.post("/update_credit_card_due_date_reference")
async def update_credit_card_due_date_reference(
    modified_credit_card_instance: CreditCardDueDateReferenceUpdate,
    authorization: str = Depends(apikey_scheme),
):
    """
    Retrieve credit card instances that belong to the logged-in user
    """
    verify_auth_header(authorization=authorization)

    _logger.debug("Instance to be modified: %s", modified_credit_card_instance)
    # prepare the request
    request = (
        supabase()
        .table("credit_card_instance")
        .update(modified_credit_card_instance.model_dump())
        .eq("id", modified_credit_card_instance.id)
    )

    # build the headers for the request then update the header
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)

    _logger.debug("Sending update command")
    # execute the command
    response = send_execute_commnad(request=request)

    # return the dataclass
    return response.model_dump()
