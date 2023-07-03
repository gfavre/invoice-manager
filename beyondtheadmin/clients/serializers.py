from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    dashboard_url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            "client_type",
            "company_name",
            "contact_first_name",
            "contact_last_name",
            "contact_email",
            "address",
            "zip_code",
            "city",
            "country",
            "language",
            "currency",
            "payment_delay_days",
            "vat_rate",
            "default_hourly_rate",
            "email_template",
            "slug",
            "invoice_current_count",
            "company",
            "url",
            "dashboard_url",
            "name",
        )

    def get_dashboard_url(self, obj: Client):
        return obj.get_absolute_url()

    def get_name(self, obj: Client):
        return obj.name

    def get_url(self, obj: Client):
        return obj.api_url

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=validated_data.keys())
        return instance


class ClientListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    dashboard_url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ("id", "name", "slug", "language", "currency", "url", "dashboard_url")

    def get_url(self, obj: Client):
        return obj.api_url

    def get_dashboard_url(self, obj: Client):
        return obj.dashboard_url
