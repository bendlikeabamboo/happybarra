import logging

from fastapi import APIRouter

from happybarra.backend.dependencies import supabase
from happybarra.backend.services.helpers import async_logged

#
# Create logger
_logger = logging.getLogger("happybarra.backend.routers.banks")


router = APIRouter(prefix="/api/v1/banks", tags=["banks"])


@async_logged(_logger)
@router.get(
    "/{bank_id}",
)
async def yoink_bank_by_id(id: str = ""):
    """
    Retrieve the bank using its UUID in the happybarra database.
    """
    # Look for the bank in the database
    response = supabase.table("bank").select("*").eq("id", id).execute()
    _logger.debug(response)

    # return the row
    return dict(response)["data"][0]


@async_logged(_logger)
@router.get(
    "/{bank_name}",
)
async def yoink_bank_by_legal_name(name: str = ""):
    """
    Attempt to retrieve the bank object by its legal name. For example, we're going to l
    look for the legal name __Bank of the Philippines Islands__ in the database.
    """
    # Look for the bank in the database
    response = supabase.table("bank").select("*").eq("name", id).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items. \n%s"
        else:
            msg = "Database did not return anything. \n%s"
        _logger.error(msg % assert_error)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]


@async_logged(_logger)
@router.get(
    "/{bank_alias}",
)
async def yoink_bank_by_streetname(alias: str = ""):
    """
    Attempt to retrieve the bank object by its alias or common name. For example,
    instead of looking for the legal name __Bank of the Philippines Islands__, we're
    going to look for its common name, __BPI__
    """
    # Look for the bank in the database
    response = supabase.table("bank").select("*").eq("alias", id).execute()
    _logger.debug(response)

    # validation: ensure that the query returned only one row
    try:
        assert len(dict(response)["data"]) == 1
    except AssertionError as assert_error:
        if len(dict(response)["data"]) > 1:
            msg = "Error: database returned multiple items. \n%s"
        else:
            msg = "Database did not return anything. \n%s"
        _logger.error(msg % assert_error)
        raise AssertionError(msg)

    # return the row
    return dict(response)["data"][0]
