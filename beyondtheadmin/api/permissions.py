from rest_framework.permissions import IsAuthenticated


class IsCompanyOwnedByUser(IsAuthenticated):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.company.users.filter(id=request.user.id).exists()
