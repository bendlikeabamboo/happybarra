import logging
from typing import List

import requests

from .constants import BACKEND_URL
from .helpers import build_authorization_header

__all__ = [
    "delete_due",
    "get_installment_by_name",
    "bulk_create_new_installment_schedules",
    "create_new_installment",
]

_logger: logging.Logger = logging.getLogger(__name__)


API_GET_DUES_SCHEDULE = f"{BACKEND_URL}/api/v1/dues/"
API_DELETE_DUE = f"{BACKEND_URL}/api/v1/dues/"


def delete_due(id: str) -> requests.Response:
    headers = build_authorization_header()
    response = requests.delete(API_DELETE_DUE + id, headers=headers)
    return response


def get_installment_by_name(name: str, headers: dict) -> dict:
    _logger.debug("Fetching credit card installment by name")
    response = requests.get(
        f"{BACKEND_URL}/api/v1/dues/credit_card_installment/{name}", headers=headers
    )
    return response


def bulk_create_new_installment_schedules(
    *, data: dict | List[dict], headers: dict
) -> requests.Response:
    _logger.debug("Creating new installment schedules...")
    response = requests.post(
        f"{BACKEND_URL}/api/v1/dues/credit_card_installment_schedule",
        headers=headers,
        json=data,
    )
    return response


def create_new_installment(
    *, data: dict | List[dict], headers: dict
) -> requests.Response:
    _logger.debug("Creating new installment instance...")
    response = requests.post(
        f"{BACKEND_URL}/api/v1/dues/credit_card_installment", headers=headers, json=data
    )
    return response
