from rest_framework import viewsets
from .serializers import CustomCustomerSerializer, CustomAdminSerializer
from .models import CustomUser
from .permissions import IsStaffOrAdmin, CustomUserPermission


class CustomClientViewSet(viewsets.ModelViewSet):

    serializer_class = CustomCustomerSerializer
    permission_classes = [CustomUserPermission]
    queryset = CustomUser.objects.filter(is_staff=False)

    def get_queryset(self):

        queryset = super().get_queryset()

        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset

        queryset = queryset.filter(id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):

        user = serializer.save(is_staff=False, is_superuser=False, role='customer')
        user.set_password(user.password)
        user.save(update_fields=['password'])


class CustomAdminViewSet(viewsets.ModelViewSet):

    serializer_class = CustomAdminSerializer
    queryset = CustomUser.objects.filter(is_staff=True)
    permission_classes = [IsStaffOrAdmin]

    def perform_create(self, serializer):

        user = serializer.save(is_staff=True, is_superuser=True, role='admin')
        user.set_password(user.password)
        user.save(update_fields=['password'])


class AllUsersViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomAdminSerializer
    permission_classes = [IsStaffOrAdmin]
