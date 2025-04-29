import datetime as dt
import logging
from types import NoneType
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import AfterValidator, BaseModel, field_serializer

from happybarra.backend.dependencies import (
    Depends,
    add_authorization_header,
    apikey_scheme,
    get_user_id,
    send_execute_command,
    supabase,
    verify_auth_header,
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


def is_float(input: str) -> float:
    try:
        return float(input)
    except ValueError as err:
        raise err


def is_uuid(input: UUID) -> str:
    try:
        return str(input)
    except ValueError as err:
        raise err


@router.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(msg="Dues is healthy 🥹")


class CreditCardInstallment(BaseModel):
    id: UUID
    created_at: dt.datetime
    name: str
    credit_card_instance_id: UUID
    user_id: UUID
    amount_type: str
    amount: Annotated[float, AfterValidator(is_float)]


class CreditCardInstallmentsGetResponse(BaseModel):
    data: List[CreditCardInstallment]
    count: NoneType | int


@router.post("/credit_card_installment")
async def add_credit_card_installment(
    credit_card_installment_form: CreditCardInstallmentForm,
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)

    # check if installment name is being used/have been used before
    existing_installments = await get_credit_card_installment(
        authorization=authorization
    )
    existing_names = [datum["name"] for datum in existing_installments.data]
    if credit_card_installment_form.name in existing_names:
        raise HTTPException(
            status_code=409,
            detail="Installment name already exists. Choose a different one.",
        )

    user_id = get_user_id(authorization=authorization)

    post_request = CreditCardInstallmentPutRequest(
        name=credit_card_installment_form.name,
        credit_card_instance_id=credit_card_installment_form.credit_card_instance_id,
        amount_type=credit_card_installment_form.amount_type,
        amount=credit_card_installment_form.amount,
        user_id=user_id,
    )
    request = (
        supabase()
        .table("credit_card_installment")
        .insert(post_request.model_dump(), returning="representation")
    )
    request = add_authorization_header(authorization=authorization, request=request)
    send_execute_command(request)

    # check if installment is indeed created
    existing_installments = await get_credit_card_installment(
        authorization=authorization
    )
    existing_names = {datum["name"]: datum for datum in existing_installments.data}
    if credit_card_installment_form.name not in existing_names:
        raise HTTPException(
            status_code=422,
            detail="Insert request successful but double-checking failed",
        )
    return CreditCardInstallment(**existing_names[credit_card_installment_form.name])


@router.get("/credit_card_installments/")
async def get_credit_card_installment(
    authorization=Depends(apikey_scheme),
) -> CreditCardInstallmentsGetResponse:
    request = supabase().table("credit_card_installment").select("*")
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


class CreditCardInstallmentScheduleForm(BaseModel):
    credit_card_installment_id: UUID
    bill_date: dt.date
    statement_date: dt.date
    due_date: dt.date
    amount: float

    @field_serializer("credit_card_installment_id")
    def serialize_uuid(self, credit_card_installment_id: UUID) -> str:
        return str(credit_card_installment_id)

    @field_serializer("bill_date", "statement_date", "due_date")
    def serialize_date(self, date: dt.date) -> str:
        return date.strftime("%Y-%m-%d")


@router.post("/credit_card_installment_schedule")
async def create_credit_card_installment_schedule(
    form: CreditCardInstallmentScheduleForm | List[CreditCardInstallmentScheduleForm],
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)
    user_id = get_user_id(authorization=authorization)

    if not isinstance(form, list):
        request_body = form.model_dump()
        request_body["user_id"] = user_id
    else:
        request_body: List[dict] = []
        for row in form:
            row = row.model_dump()
            row["user_id"] = user_id
            request_body.append(row)

    request = supabase().table("credit_card_installment_schedule").insert(request_body)
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


@router.get("/credit_card_installment/{name}")
async def get_credit_card_installment_by_name(
    name: str,
    authorization=Depends(apikey_scheme),
) -> CreditCardInstallmentsGetResponse:
    verify_auth_header(authorization=authorization)
    request = supabase().table("credit_card_installment").select("*").eq("name", name)
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


@router.get("/credit_card_installment_schedule/{name}")
async def get_credit_card_installment_schedule_by_name(
    name: str,
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)
    installment_by_name_response = await get_credit_card_installment_by_name(
        name=name, authorization=authorization
    )
    installment_id = installment_by_name_response.data[0]["id"]
    request = (
        supabase()
        .table("credit_card_installment_schedule")
        .select("*")
        .eq("credit_card_installment_id", installment_id)
    )
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


@router.get("/")
async def get_dues(
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)
    request = supabase().table("financial_commitment_schedule").select("*")
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


@router.delete("/{due_id}")
async def delete_due(
    due_id: UUID,
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)
    request = (
        supabase()
        .table("financial_commitment")
        .select("id, source_type")
        .eq("id", due_id)
    )
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)

    data_results: List[dict] = response.model_dump().get("data", {})
    source_type = data_results[0].get("source_type")

    request = supabase().table(source_type).delete().eq("id", due_id)
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)

    return response
