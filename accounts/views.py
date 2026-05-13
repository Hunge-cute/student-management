from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrStaff]
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
