from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Bank, Company


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = (
            "swift",
            "name",
            "address",
            "zip_code",
            "city",
            "country",
        )


class IDECompanySerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(required=False)
    zip_code = serializers.CharField(max_length=5, required=False)
    city = serializers.CharField(max_length=255, required=True)
    vat_id = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=2, required=False)


class IBANInfosSerializer(serializers.Serializer):
    iban = serializers.CharField(max_length=34)
    iban_valid = serializers.BooleanField()
    bank = BankSerializer(read_only=True, many=False)

    class Meta:
        fields = (
            "iban",
            "iban_valid",
            "bank",
        )


class CompanyListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "name",
            "id",
            "url",
            "enable_vat",
            "vat_rate",
            "default_hourly_rate",
            "payment_delay_days",
        )

    def get_url(self, obj: Company):
        return obj.api_url


class CompanySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "address",
            "zip_code",
            "city",
            "country",
            "phone",
            "additional_phone",
            "email",
            "website",
            "enable_vat",
            "vat_rate",
            "vat_id",
            "default_hourly_rate",
            "payment_delay_days",
            "name_for_bank",
            "bank",
            "bic",
            "iban",
            "logo",
            "contrast_color",
            "signature_text",
            "signature_image",
            "bcc_email",
            "from_email",
            "thanks",
            "email_signature",
            "invoice_note",
        )

    def get_cc(self, obj):
        return obj.country.code
