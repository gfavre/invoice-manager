import requests


class OpenIban:
    URL = "https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"

    @staticmethod
    def validate_iban(iban):
        try:
            response = requests.get(url=OpenIban.URL.format(iban=iban))
        except requests.exceptions.RequestException:
            return {"valid": False}
        response_json = response.json()
        return {
            "valid": response_json.get("valid"),
            "bank_name": response_json.get("bankData", {}).get("name", ""),
            "bank_bic": response_json.get("bankData", {}).get("bic", ""),
            "bank_code": response_json.get("bankData", {}).get("bankCode", ""),
        }
