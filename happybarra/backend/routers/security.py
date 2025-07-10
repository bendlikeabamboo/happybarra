import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from gotrue.types import AuthResponse
from pydantic import BaseModel

from happybarra.backend.dependencies import (
    supabase,
)
from happybarra.backend.services.helpers import async_logged

#
# Create logger
_logger = logging.getLogger("happybarra.backend.routers.security")

router = APIRouter(prefix="/api/v1/security", tags=["security"])


class UserCredentials(BaseModel):
    user: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class User(BaseModel):
    id: str
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


@async_logged(_logger)
@router.post(
    "/login",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response = None,
) -> LoginResponse:
    """
    Retrieve an access token from supabase auth.
    """
    print(form_data)
    auth_call: AuthResponse = supabase().auth.sign_in_with_password(
        {
            "email": form_data.username,
            "password": form_data.password,
        }
    )
    print(auth_call.model_dump())
    response.headers["X-Refresh-Token"] = auth_call.session.refresh_token
    return LoginResponse(
        access_token=auth_call.session.access_token,
        token_type="bearer",
        refresh_token=auth_call.session.refresh_token,
    )
