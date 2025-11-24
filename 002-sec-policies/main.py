import os
import logging
import sys
import logging
import urllib3
import pkgutil
import importlib
from typing import Optional
from mcp.server.fastmcp import FastMCP
from panos import firewall


# Logging
## Logs directory
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "mcp_server.log")

# Configure logger
logger = logging.getLogger("palo_mcp")
logger.setLevel(logging.INFO)
logger.propagate = False

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
file_handler.setFormatter(file_formatter)

# Attach handlers ONLY once
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# Disable CERT warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Firewall Configuration - env
FIREWALL_IP = os.getenv("FIREWALL_IP", "1.2.3.4")
API_KEY = os.getenv("FIREWALL_API_KEY", "api-key")

if not API_KEY:
    raise ValueError("FIREWALL_API_KEY environment variable is required")


# Firewall Object
_firewall_instance: Optional[firewall.Firewall] = None

def get_firewall() -> firewall.Firewall:
    global _firewall_instance

    if _firewall_instance is None:
        try:
            _firewall_instance = firewall.Firewall(FIREWALL_IP, api_key=API_KEY)
            logger.info(f"Connected to firewall at {FIREWALL_IP}")
        except Exception as e:
            logger.error(f"Failed to connect to firewall: {str(e)}")
            raise Exception(f"Failed to connect to firewall: {str(e)}")

    return _firewall_instance


# MCP Server
server = FastMCP("Palo Alto Firewall Manager")


## Load MCP Tools, other .py
def load_tools():
    """
    Load tool modules inside tools/ folder, but only log:
    - successful tool registrations
    - errors
    - final summary
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)

    tools_path = os.path.join(base_dir, "tools")

    registered = []
    errors = []

    for finder, module_name, ispkg in pkgutil.walk_packages([tools_path], prefix="tools."):
        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "register"):
                module.register(server)
                registered.append(module_name)
            # else: silent ignore: package folders, helpers, etc.

        except Exception as e:
            errors.append((module_name, str(e)))

    # Final summary:
    logger.info(f"Loaded {len(registered)} MCP tool modules:")
    for m in registered:
        logger.info(f"  ✓ {m}")

    if errors:
        logger.error(f"Failed to load {len(errors)} modules:")
        for mod, err in errors:
            logger.error(f"  ✗ {mod} → {err}")


if __name__ == "__main__":
    load_tools()
    server.run(transport="stdio")
