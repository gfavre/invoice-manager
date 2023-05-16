from django.core.files.base import ContentFile

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from beyondtheadmin.users.models import User

from ..models import Company
from ..serializers import CompanyListSerializer, CompanySerializer, IDECompanySerializer
from ..utils.iban import OpenIban
from ..utils.zefix import get_detail, search_zefix


MAX_NB_SEARCH_RESULTS = 15
QUERY_MIN_LENGTH = 3


class CompanySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get("q")
        try:
            nb_results = int(request.query_params.get("nb"))
        except (ValueError, TypeError):
            nb_results = MAX_NB_SEARCH_RESULTS
        data = []
        if query_string and len(query_string) >= QUERY_MIN_LENGTH:
            data = search_zefix(query_string)
        serializer = IDECompanySerializer(data=data[:nb_results], many=True)
        serializer.is_valid()
        return Response(serializer.data)


class IBANSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get("q")
        data = []
        if query_string:
            data = OpenIban.validate_iban(query_string)
        return Response(data)


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get("uid")
        data = []
        if query_string:
            data = get_detail(query_string)
        data["country"] = "CH"
        serializer = IDECompanySerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)


class CompaniesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        return self.serializer_class

    def get_queryset(self):
        user: User = self.request.user
        return user.companies.all()

    def perform_create(self, serializer):
        company = serializer.save()
        company.users.add(self.request.user)

    def _update_file_for_field(self, request, field_name):
        company = self.get_object()
        file_name = request.META.get("HTTP_X_FILE_NAME")
        file_data = ContentFile(request.body)
        if getattr(company, field_name):
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_201_CREATED
        getattr(company, field_name).save(file_name, file_data, save=True)
        return Response({}, status=response_status)

    @action(detail=True, methods=["put"])
    def update_logo(self, request, pk=None):
        return self._update_file_for_field(request, "logo")

    @action(detail=True, methods=["put"])
    def update_signature_image(self, request, pk=None):
        return self._update_file_for_field(request, "signature_image")
