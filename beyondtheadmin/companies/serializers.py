from rest_framework import serializers

from .models import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("swift", "name", "address", "zip_code", "city", "country", )


class IDECompanySerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(required=False)
    zip_code = serializers.CharField(max_length=5, required=False)
    city = serializers.CharField(max_length=255, required=True)
    vat_id = serializers.CharField(max_length=20)


class IBANInfosSerializer(serializers.Serializer):
    iban = serializers.CharField(max_length=34)
    iban_valid = serializers.BooleanField()
    bank = BankSerializer(read_only=True, many=False)

    class Meta:
        fields = ("iban", "iban_valid", "bank", )




