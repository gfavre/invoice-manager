from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import IDECompanySerializer
from ..ide_utils import search_company


class CompanySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_string = request.query_params.get('q')
        data = []
        if query_string:
            data = search_company(query_string)
        serializer = IDECompanySerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)
