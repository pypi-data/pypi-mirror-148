"""
These are framework specific environment variables.
The .env file is provided "out of the box" with Solace.
The following variables are used through out this framework
as needed, but application developers can set whatever vars
they want to in the .env file as well.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENV_NAME = os.environ.get('ENV_NAME', 'solace-env')
ENV_TYPE = os.environ.get('ENV_TYPE', 'dev')

TRACERS_ENABLED = os.environ.get('TRACERS_ENABLED', False)

LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO").upper()
LOG_FILE = os.environ.get('LOG_FILE')
LOG_TYPE = os.environ.get('LOG_TYPE', "text")
LOG_FORMAT = os.environ.get('LOG_FORMAT')

STATIC_ASSETS_DIR = os.environ.get("STATIC_ASSETS_DIR", None)
STATIC_ASSETS_URL = os.environ.get("STATIC_ASSETS_URL", None)
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", None)

HTTP_EXCEPTION_TYPE = os.environ.get("HTTP_EXCEPTION_TYPE", "text") # can be set to text, html or json