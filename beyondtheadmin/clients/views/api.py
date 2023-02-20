from rest_framework import viewsets

from ..models import Client
from ..serializers import ClientSimpleSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSimpleSerializer

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class  # ClientListSerializer
        return self.serializer_class
