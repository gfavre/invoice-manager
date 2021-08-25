# -*- coding: utf-8 -*-
from beyondtheadmin.companies.models import Company


def add_companies_to_context(request):
    if not (hasattr(request, 'user') and request.user.is_authenticated):
        return {}
    return {
        'companies': Company.objects.filter(users=request.user)
    }
