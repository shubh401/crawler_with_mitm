from collections import defaultdict
from copy import deepcopy

import traceback
import asyncio
import logging
import shutil
import json
import sys
import os

# BASE LOGGER
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename=f"/app/extensions/logs/{os.getenv('TEST_ID')}.log",
    filemode="a+"
)
logging.getLogger("urllib3").setLevel(logging.ERROR)

# CRAWL CONFIG
ALLOWED_RETRIALS = 5
TEST_TYPE = "organic"
TMP_PATH = "/tmp/chromiumDataDir/"

# CONTEXT CONFIG
EXTENSION_DIR = "/app/extensions/"
LAUNCH_ARGS = {
    "headless": False,
    "timeout": 30000,
    "ignore_https_errors": True,
    "no_viewport": True,
    "ignore_default_args": ["--enable-automation"],
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "args": [
        '--no-first-run',
        '--disable-infobars',
        '--disable-setuid-sandbox',
        '--ignore-certificate-errors',
        '--disable-software-rasterizer',
        '--start-maximized',
        '--shm-size=2G',
        '--allow-running-insecure-content',
        '--ignore-certificate-errors-spki-list',
        '--disable-gpu',
        '--allow-future-manifest-version',
        '--allow-legacy-extension-manifests',
    ]
}

# PAGE CONFIG
CRAWL_TIMEOUT = 10000
CRAWL_TIMEOUT_II = 5000 # Extension Detection Page
NAVIGATION_TIMEOUT = 30000
WAIT_TIMEOUT = 10
