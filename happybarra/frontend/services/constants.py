import os
from typing import TypeVar

import dotenv

__all__ = [
    "CONFIG_KEY",
    "CONFIG_USE_MOCKS_HOOK",
    "CONFIG_BYPASS_LOGIN_HOOK",
    "CONFIG_DEV_MODE_HOOK",
    "BACKEND_URL",
]

CONFIG_KEY = "happybarra_config"
CONFIG_USE_MOCKS_HOOK = f"{CONFIG_KEY}__use_mocks"
CONFIG_BYPASS_LOGIN_HOOK = f"{CONFIG_KEY}__bypass_login"
CONFIG_DEV_MODE_HOOK = f"{CONFIG_KEY}__dev_mode"

dotenv.load_dotenv()
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")
