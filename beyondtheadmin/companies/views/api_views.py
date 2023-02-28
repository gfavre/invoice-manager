from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
        return self.request.user.companies.all()
