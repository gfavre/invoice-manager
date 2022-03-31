from rest_framework import serializers


class IDECompanySerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=255)
    address = serializers.CharField()
    zip_code = serializers.CharField(max_length=5)
    city = serializers.CharField(max_length=255)
    vat_id = serializers.CharField(max_length=20)
