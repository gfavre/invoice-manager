from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = "__all__"

    def get_url(self, obj: Client):
        return obj.api_url


class ClientListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ("id", "name", "slug", "language", "currency", "url")

    def get_url(self, obj: Client):
        return obj.api_url
