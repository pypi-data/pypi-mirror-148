import os
from dotenv import load_dotenv

load_dotenv()

ENV_NAME = os.environ.get('ENV_NAME', 'solace-env')
ENV_TYPE = os.environ.get('ENV_TYPE', 'dev')

LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO").upper()
LOG_FILE = os.environ.get('LOG_FILE')
LOG_TYPE = os.environ.get('LOG_TYPE', "text")
LOG_FORMAT = os.environ.get('LOG_FORMAT')

STATIC_ASSETS_DIR = os.environ.get("STATIC_ASSETS_DIR", "static")
STATIC_ASSETS_URL = os.environ.get("STATIC_ASSETS_URL", "/static")
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "templates")
