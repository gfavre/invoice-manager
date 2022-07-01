from rest_framework import serializers

from .products import PRODUCTS


class ProductSerializer(serializers.Serializer):
    code = serializers.ChoiceField(choices=list(PRODUCTS.keys()))

