from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = "__all__"

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

    class Meta:
        model = Client
        fields = ("id", "name", "slug", "language", "currency", "url")

    def get_url(self, obj: Client):
        return obj.api_url
