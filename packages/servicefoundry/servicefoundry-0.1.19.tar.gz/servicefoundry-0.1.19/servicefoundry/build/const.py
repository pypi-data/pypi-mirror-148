import os
from pathlib import Path

SERVICE_FOUNDRY_SERVER = (
    os.environ.get("SFY_SERVER")
    or "https://sf-server.tfy-ctl-us-east-1-develop.develop.truefoundry.io"
)

# Auth related config
# TODO: Call service foundry to get this.
DEFAULT_TENANT_ID = (
    os.environ.get("SFY_TENANT_ID")
    or "895253af-ec9d-4be6-83d1-6f248e644e79"
)
AUTH_UI = (
    os.environ.get("SFY_AUTH_UI") or "https://app.develop.truefoundry.io"
)
AUTH_SERVER = (
    os.environ.get("SFY_AUTH_SERVER")
    or "https://auth-server.tfy-ctl-us-east-1-develop.develop.truefoundry.io"
)
# AUTH_SERVER = "http://localhost:3000"
SESSION_FILE = f"{str(Path.home())}/.truefoundry"

# Build related Config
SERVICE_DEF_FILE_NAME = "servicefoundry.yaml"
BUILD_DIR = ".servicefoundry"

COMPONENT = "Component"
BUILD_PACK = "BuildPack"

# Polling during login redirect
MAX_POLLING_RETRY = 100
POLLING_SLEEP_TIME_IN_SEC = 4

# Refresh access token cutoff
REFRESH_ACCESS_TOKEN_IN_SEC = 10 * 60
