import requests
import sys
import uuid
import platform
import random

ACCOUNT_ID = "c433938c-8a20-41d5-aca3-0f2564693b5e"
LICENSE_KEY = input("🔑 Enter your license key: ").strip()

# Generate random exit codes for this run
SUCCESS_CODE = random.randint(10000, 99999)
FAIL_CODE = random.randint(10000, 99999)

hwid = str(uuid.getnode()) + "_" + platform.node()

# Print the exit codes so Batch can read them
print(f"__EXIT_CODES__ {SUCCESS_CODE} {FAIL_CODE}")

def validate_license(key):
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/actions/validate-key"
    payload = {"meta": {"key": key}}

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except:
        sys.exit(FAIL_CODE)

    data = r.json()
    if not data.get("meta", {}).get("valid", False):
        sys.exit(FAIL_CODE)

    license_id = data.get("data", {}).get("id")
    return license_id

def register_machine(license_id, hwid):
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
    except:
        sys.exit(FAIL_CODE)

license_id = validate_license(LICENSE_KEY)
register_machine(license_id, hwid)