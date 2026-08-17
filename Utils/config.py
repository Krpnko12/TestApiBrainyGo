"""Configuration loaded from environment variables."""

import os

BASE_URL = os.getenv("BRAINYGO_BASE_URL", "").rstrip("/")
USERNAME = os.getenv("BRAINYGO_USERNAME", "")
PASSWORD = os.getenv("BRAINYGO_PASSWORD", "")
REQUEST_TIMEOUT = float(os.getenv("BRAINYGO_REQUEST_TIMEOUT", "10"))
