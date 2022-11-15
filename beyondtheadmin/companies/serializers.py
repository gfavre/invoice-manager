from rest_framework import serializers


class IDECompanySerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(required=False)
    zip_code = serializers.CharField(max_length=5, required=False)
    city = serializers.CharField(max_length=255, required=True)
    vat_id = serializers.CharField(max_length=20)


class IBANInfosSerializer(serializers.Serializer):
    iban = serializers.CharField(max_length=34)
    bic = serializers.CharField(max_length=11)
    bank_name = serializers.CharField(max_length=255)
    bank_address = serializers.CharField(max_length=255)
    bank_zip_code = serializers.CharField(max_length=5)
    bank_city = serializers.CharField(max_length=255)
