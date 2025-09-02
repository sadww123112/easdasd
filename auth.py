import requests
import sys
import uuid
import platform
import random

# ------------------------
# CONFIG
# ------------------------
ACCOUNT_ID = "your-account-id"  # Replace with your Keygen.sh account ID

# Generate random exit codes for this run
SUCCESS_CODE = random.randint(10000, 99999)
FAIL_CODE = random.randint(10000, 99999)

# ------------------------
# FUNCTIONS
# ------------------------
def get_hwid():
    """Generate a device fingerprint (HWID)"""
    return str(uuid.getnode()) + "_" + platform.node()

def validate_license(key):
    """Validate the license key with Keygen.sh"""
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/actions/validate-key"
    payload = {"meta": {"key": key}}

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception:
        sys.exit(FAIL_CODE)

    data = r.json()
    if not data.get("meta", {}).get("valid", False):
        sys.exit(FAIL_CODE)

    license_id = data.get("data", {}).get("id")
    return license_id

def register_machine(license_id, hwid):
    """Register HWID as a machine under this license"""
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/{license_id}/machines"
    payload = {"meta": {"fingerprint": hwid}}

    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 201:
            sys.exit(SUCCESS_CODE)
        elif r.status_code == 422:
            sys.exit(FAIL_CODE)
        else:
            sys.exit(FAIL_CODE)
    except Exception:
        sys.exit(FAIL_CODE)

# ------------------------
# MAIN
# ------------------------
if __name__ == "__main__":
    LICENSE_KEY = input("Enter your license key: ").strip()
    hwid = get_hwid()
    license_id = validate_license(LICENSE_KEY)
    register_machine(license_id, hwid)

    # Print exit codes for Batch to read dynamically
    print(f"__EXIT_CODES__ {SUCCESS_CODE} {FAIL_CODE}")
