import logging
import os

from dotenv import load_dotenv
from supabase import AsyncClient, create_async_client

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger("happybarra.backend.dependencies")

_logger.debug("Loading environment variables.")
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

_logger.debug("Creating supabase client")
supabase: AsyncClient = create_async_client(url, key)
