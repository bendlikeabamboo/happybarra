import logging

from fastapi import APIRouter
from pydantic import BaseModel
from supabase import AsyncClient

from happybarra.backend.dependencies import supabase
from happybarra.backend.services.helpers import async_logged

#
# Create logger
_logger = logging.getLogger("happybarra.backend.routers.security")

router = APIRouter(prefix="/api/v1/security", tags=["Security"])


class UserCredentials(BaseModel):
    user: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str


@async_logged(_logger)
@router.post(
    "/login",
)
async def enter_matrix(user_credentials: UserCredentials) -> LoginResponse:
    """
    Enter the matrix
    """
    awaited_supabase: AsyncClient = await supabase
    response = awaited_supabase.auth.sign_in_with_password(
        {
            "email": user_credentials.user,
            "password": user_credentials.password,
        }
    )

    awaited_response = await response
    login_response = LoginResponse(
        access_token=dict(dict(awaited_response)["session"])["access_token"],
        refresh_token=dict(dict(awaited_response)["session"])["refresh_token"],
    )
    return login_response


@async_logged(_logger)
@router.post(
    "/refresh",
)
async def refresh_matrix(refresh_token: RefreshToken):
    """
    Enter the matrix
    """
    awaited_supabase: AsyncClient = await supabase
    response = awaited_supabase.auth.refresh_session(**refresh_token.model_dump())

    awaited_response = await response
    login_response = awaited_response
    return login_response
