import requests
import sys

# ضع حسابك في keygen.sh
ACCOUNT_ID = "c433938c-8a20-41d5-aca3-0f2564693b5e"   # استبدلها بالـ Account ID حقك

def check_license(key: str) -> bool:
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/actions/validate-key"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
    payload = {
        "meta": {
            "key": key
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("meta", {}).get("valid", False)
    else:
        return False

def main():
    # هنا المستخدم يدخل الليسن
    license_key = input("license Key").strip()

    if check_license(license_key):
        print("valid")
        sys.exit(0)
    else:
        print("invalid")
        sys.exit(1)

if __name__ == "__main__":
    main()
