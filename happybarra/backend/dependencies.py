import logging
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, Header
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pydantic import BaseModel
from supabase import Client, create_client

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger("happybarra.backend.dependencies")

_logger.debug("Loading environment variables.")
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/security/login")
apikey_scheme = APIKeyHeader(name="Authorization")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


def supabase() -> Client:
    _logger.debug("Creating supabase client")
    return create_client(url, key)


class AccessTokens(BaseModel):
    access_token: str
    refresh_token: str = None


async def get_authed_supabase_client(
    token: Annotated[LoginResponse, Depends(oauth2_scheme)],
    x_refresh_token: Annotated[str | None, Header()] = None,
) -> Client:
    """
    Get the matrix???
    """
    session: Client = supabase()
    try:
        session.auth.set_session(access_token=token, refresh_token=x_refresh_token)
    except AttributeError as err:
        _logger.debug(
            "Fail to authenticate with supabase due to missing refresh token. \n %s",
            err,
        )

    # TODO: Catch errors here
    return session


async def rcv_acc_token(token: str):
    return {"Authorization": f"Bearer {token}"}
