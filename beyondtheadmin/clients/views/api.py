from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from beyondtheadmin.api.permissions import IsCompanyOwnedByUser

from ..models import Client
from ..serializers import ClientListSerializer, ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsCompanyOwnedByUser]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset().filter(company__users=self.request.user)
        if "company_uuid" in self.request.query_params:
            company_uuid = self.request.query_params.get("company_uuid")
            queryset = queryset.filter(company_id=company_uuid)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ClientListSerializer
        return self.serializer_class
