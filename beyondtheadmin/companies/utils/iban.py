import requests

from ..models import Bank
from ..serializers import BankSerializer


class OpenIban:
    URL = "https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"

    @staticmethod
    def validate_iban(iban):
        try:
            response = requests.get(url=OpenIban.URL.format(iban=iban))
        except requests.exceptions.RequestException:
            return {"valid": False}
        response_json = response.json()
        bank_code = response_json.get("bankData", {}).get("bankCode", "")
        print(response_json)
        try:
            bank = Bank.objects.get(code=bank_code)
            bank_data = BankSerializer(instance=bank).data
        except (Bank.DoesNotExist, ValueError):
            bank_data = None

        return {
            "valid": response_json.get("valid"),
            "iban": response_json.get("iban"),
            "bank": bank_data,
        }
