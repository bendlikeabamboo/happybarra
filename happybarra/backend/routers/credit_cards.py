import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from gotrue import UserResponse
from pydantic import BaseModel

from happybarra.backend.dependencies import (
    APIResponse,
    Client,
    SyncSelectRequestBuilder,
    apikey_scheme,
    get_authed_supabase_client,
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


class CreditCardCreationForm(BaseModel):
    name: str
    credit_card: str
    statement_day: str
    due_date_reference: int


def validate_if_response_is_one(response: APIResponse, query: str) -> APIResponse:
    if len(response.data) == 0:
        raise HTTPException(
            status_code=404,
            detail={"msg": f"Resource not found: {query}"},
        )
    elif len(response.data) != 1:
        raise HTTPException(
            status_code=409,
            detail={"msg": f"Data fetched is more than one: {query}"},
        )


@async_logged(_logger)
@router.put("")
async def add_credit_card(
    credit_card_to_add: CreditCardCreationForm,
    authorization: str = Depends(apikey_scheme),
):
    """
    Add credit card to user
    """
    verify_auth_header(authorization=authorization)

    # first get the id of the credit card
    response: APIResponse = (
        supabase()
        .table("credit_card")
        .select("*")
        .eq("name", credit_card_to_add.credit_card)
        .execute()
    )

    # validate the fetched credit card
    validate_if_response_is_one(response, query=credit_card_to_add.credit_card)

    # if validation passed, get the id
    fetched_credit_card_id = response.data[0]["id"]

    # then get the user
    jwt_key = authorization[len("Bearer ") :]
    _logger.debug("Authorization being used: %s", jwt_key)
    response: UserResponse = supabase().auth.get_user(jwt_key)
    user_id = response.user.id

    # use the fetched credit card and fetched user to build the request
    request_body = {}
    request_body["name"] = credit_card_to_add.name
    request_body["statement_day"] = str(credit_card_to_add.statement_day)
    request_body["due_date_reference"] = int(credit_card_to_add.due_date_reference)
    request_body["credit_card_id"] = fetched_credit_card_id
    request_body["user_id"] = user_id

    request = supabase().table("credit_card_instance").insert(request_body)

    # build the headers for the request then update the header
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)

    response = request.execute()
    return response.model_dump()


@async_logged(_logger)
@router.get("")
async def get_credit_cards(authorization: str = Depends(apikey_scheme)):
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


class CreditCardName(BaseModel):
    name: str


def setup_supabase_request_headers(
    request: SyncSelectRequestBuilder, authorization: dict
) -> SyncSelectRequestBuilder:
    """
    Add authorization to the headers of the supabase request.
    """
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)
    return request


@async_logged(_logger)
@router.delete("")
async def delete_credit_card(
    credit_card_name: CreditCardName, authorization: str = Depends(apikey_scheme)
):
    _logger.debug("\n---\nBegin credit card deletion sequence...")
    _logger.debug(
        "Getting credit card id associated to the provided credit card name: %s",
        credit_card_name,
    )

    db_request = (
        supabase()
        .table("credit_card_instance")
        .select("id, name")
        .eq("name", credit_card_name.name)
    )

    db_request = setup_supabase_request_headers(db_request, authorization)

    # execute
    response: APIResponse = db_request.execute()
    del db_request

    # validate
    validate_if_response_is_one(response=response, query=credit_card_name.name)

    _logger.debug(
        "Sending delete request: %s",
        credit_card_name,
    )

    # send delete request
    id_to_delete = response.data[0]["id"]
    db_request = (
        supabase().table("credit_card_instance").delete().eq("id", id_to_delete)
    )
    db_request = setup_supabase_request_headers(db_request, authorization)
    _logger.debug(
        "Sending delete request: %s",
        credit_card_name,
    )
    response: APIResponse = db_request.execute()
    _logger.debug("Deletion sequence finished.\n---\n")

    return response
