# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'name', 'slug', 'url')

    def get_url(self, obj: Client):
        return obj.get_absolute_url()
