import requests
import sys

# ضع حسابك في keygen.sh
ACCOUNT_ID = "1a7148f1-2a51-414c-802a-6bdabf32bc6e"   # استبدلها بالـ Account ID حقك

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
    license_key = input("License Key : ").strip()

    if check_license(license_key):
        print("Checking....")
        sys.exit(0)
    else:
        print("Checking....")
        sys.exit(1)

if __name__ == "__main__":
    main()



