import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from uuid import UUID
from decimal import Decimal

from happybarra.backend.dependencies import (
    apikey_scheme,
    Depends,
    verify_auth_header,
    supabase,
    send_execute_command,
)

#
# Create logger
_logger = logging.getLogger("happybarra.backend.routers.dues")

router = APIRouter(prefix="/api/v1/dues", tags=["dues"])


class HealthResponse(BaseModel):
    msg: str


class CreditCardInstallmentForm(BaseModel):
    name: str
    credit_card_instance_id: str
    amount_type: str
    amount: float


class CreditCardInstallmentPutRequest(BaseModel):
    name: str
    credit_card_instance_id: str
    amount_type: str
    amount: float
    user_id: str


@router.get("/")
async def health() -> HealthResponse:
    return HealthResponse(msg="Dues is healthy 🥹")


@router.put("/credit_card_installment/")
async def add_credit_card_installment(
    credit_card_installment_form: CreditCardInstallmentForm,
    authorization=Depends(apikey_scheme),
):
    # Task #1: Data validate header
    verify_auth_header(authorization)

    # Task #2: Get user_id
    token = authorization[len("Bearer ") :]

    try:
        user_id = supabase().auth.get_user(jwt=token).model_dump()["user"]["id"]
    except KeyError as err:
        HTTPException(
            status_code=403,
            detail=f"Failed to authenticate user with the provided identity. {err}",
        )

    put_request = CreditCardInstallmentPutRequest(
        name=credit_card_installment_form.name,
        credit_card_instance_id=credit_card_installment_form.credit_card_instance_id,
        amount_type=credit_card_installment_form.amount_type,
        amount=credit_card_installment_form.amount,
        user_id=user_id,
    )
    _logger.debug("`put_request` %s", put_request.model_dump())
    request = (
        supabase()
        .table("credit_card_installment")
        .insert(put_request.model_dump(), returning="representation")
    )
    # build the headers for the request then update the header
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)

    response = send_execute_command(request)
    return response
