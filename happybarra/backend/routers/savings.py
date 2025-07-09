import datetime as dt
import logging
from types import NoneType
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import AfterValidator, BaseModel, field_serializer, AwareDatetime

from happybarra.backend.dependencies import (
    Depends,
    add_authorization_header,
    apikey_scheme,
    get_user_id,
    send_execute_command,
    supabase,
    verify_auth_header,
)

_logger = logging.getLogger("happybarra.backend.routers.savings")

router = APIRouter(prefix="/api/v1/savings", tags=["Savings"])


class SavingsForm(BaseModel):
    name: str
    goal: float


class SavingsPlanInsertRequest(BaseModel):
    name: str
    goal: float
    user_id: str


class SavingsDataModel(BaseModel):
    name: str
    user_id: str
    id: str
    created_at: str
    goal: float


class SavingsDataResponse(BaseModel):
    data: List[SavingsDataModel]
    count: int


@router.get("/")
async def get_savings(
    authorization=Depends(apikey_scheme),
) -> SavingsDataResponse:
    verify_auth_header(authorization=authorization)

    user_id = get_user_id(authorization=authorization)
    request = supabase().table("savings").select("*").eq("user_id", user_id)
    request = add_authorization_header(authorization=authorization, request=request)
    response = send_execute_command(request=request)
    return response


@router.post("/")
async def insert_savings(
    savings_plan_form: SavingsForm, authorization=Depends(apikey_scheme)
):
    verify_auth_header(authorization=authorization)

    user_id = get_user_id(authorization=authorization)
    savings_plan_request = SavingsPlanInsertRequest(
        name=savings_plan_form.name, goal=savings_plan_form.goal, user_id=user_id
    )
    request = (
        supabase()
        .table("savings")
        .insert(savings_plan_request.model_dump(), returning="representation")
    )
    request = add_authorization_header(authorization=authorization, request=request)
    send_execute_command(request=request)

    # check if installment is created
    savings_response = await get_savings(authorization=authorization)
    existing_savings = {datum["name"]: datum for datum in savings_response.data}
    if savings_plan_form.name not in existing_savings:
        raise HTTPException(
            status_code=422,
            detail="Insert request successful but double-checking failed",
        )

    return SavingsDataModel(**existing_savings[savings_plan_form.name])


class SavingsScheduleForm(BaseModel):
    savings_name: str
    date: dt.date
    amount: float


class SavingsScheduleInsertRequest(BaseModel):
    savings_id: str
    date: dt.date
    amount: float
    user_id: str


class SavingsScheduleDataModel(BaseModel):
    savings_id: str
    date: dt.date
    created_at: AwareDatetime
    id: str
    amount: float
    user_id: str


class SavingsScheduleDataResponse(BaseModel):
    data: List[SavingsDataModel]
    count: int


@router.get("/schedule/")
async def get_savings_schedule(
    savings_schedule_form: SavingsScheduleForm, authorization=Depends(apikey_scheme)
) -> SavingsDataResponse: ...


@router.post("/schedule")
async def insert_savings_schedule(
    savings_schedule_form: SavingsScheduleForm,
    authorization=Depends(apikey_scheme),
):
    verify_auth_header(authorization=authorization)

    user_id = get_user_id(authorization=authorization)
    savings_data: List[SavingsDataModel] = await get_savings(
        authorization=authorization
    ).data

    target_savings: SavingsDataModel = [
        savings
        for savings in savings_data
        if savings.name == savings_schedule_form.savings_name
    ]
    try:
        assert len(target_savings) == 1
    except AssertionError as er:
        _logger.error(
            "Found multiple instances of the savings name: %s",
            savings_schedule_form.savings_name,
        )
    record_to_insert = SavingsScheduleInsertRequest(
        savings_id=target_savings.id,
        date=savings_schedule_form.date,
        amount=savings_schedule_form.date,
        user_id=user_id,
    )

    # request building
    request = (
        supabase()
        .table("savings_schedule")
        .insert(record_to_insert.model_dump(), returning="representaiton")
    )

    request = add_authorization_header(authorization=authorization, request=request)
    send_execute_command(request=request)

    # TODO: Verify if savings is indeed created. Check function above.


# @router.post("/schedule")
