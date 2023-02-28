from django.http import JsonResponse


def csrf_token(request):
    return JsonResponse({"csrf_token": request.COOKIES.get("csrftoken")})
