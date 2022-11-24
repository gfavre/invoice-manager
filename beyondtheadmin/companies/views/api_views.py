from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import IDECompanySerializer
from ..utils.iban import OpenIban
from ..utils.zefix import get_detail, search_zefix


class CompanySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get("q")
        data = []
        if query_string:
            data = search_zefix(query_string)
        serializer = IDECompanySerializer(data=data, many=True)
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
        serializer = IDECompanySerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)
