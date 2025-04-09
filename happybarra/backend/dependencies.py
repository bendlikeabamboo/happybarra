import logging
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from postgrest._sync.request_builder import APIResponse, SyncSelectRequestBuilder
from postgrest.exceptions import APIError
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


def send_execute_command(request: SyncSelectRequestBuilder) -> APIResponse:
    """
    Yet another redirection so that we handle all errors in this one function.
    """
    try:
        response = request.execute()
    except APIError as err:
        headers = {
            "WWW-Authenticate": 'Bearer error="invalid_token", '
            'error_description="The access token expired"'
        }
        err_msg = f"{err}. Please login again."

        raise HTTPException(status_code=401, detail=err_msg, headers=headers)
    return response


def verify_auth_header(authorization: str):
    """
    Just to check the auth header
    """
    _logger.debug("Verifying auth headers...")
    if not authorization:
        raise HTTPException(
            status_code=401, detail="No doba doba provided. Mirku sadge."
        )
    if "Bearer " not in authorization:
        raise HTTPException(
            status_code=401, detail="doba doba seems dysfunctional. Mirku Sadge"
        )
    _logger.debug("Verifying auth headers verified.")


def get_user_id(authorization: str) -> str:
    _logger.debug("Obtaining user id...")
    token = authorization[len("Bearer ") :]

    try:
        user_id = supabase().auth.get_user(jwt=token).model_dump()["user"]["id"]
        _logger.debug("User id obtained.")
        return user_id
    except KeyError as err:
        HTTPException(
            status_code=403,
            detail=f"Failed to authenticate user with the provided identity. {err}",
        )


def add_authorization_header(
    authorization: str, request: SyncSelectRequestBuilder
) -> SyncSelectRequestBuilder:
    key_dict = {"Authorization": authorization}
    request.headers = key_dict or request.headers.update(key_dict)
    return request
