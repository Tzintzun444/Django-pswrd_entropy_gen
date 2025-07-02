from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsStaffOrAdmin
from .serializers import PasswordGenerationSerializer, PasswordModelSerializer
from .models import Password
from .permissions import PasswordPermission


class PasswordViewSet(viewsets.GenericViewSet):

    queryset = Password.objects.all()
    serializer_class = PasswordGenerationSerializer
    permission_classes = [PasswordPermission]

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return PasswordGenerationSerializer
        return PasswordModelSerializer

    def create(self, request):

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        response_serializer = PasswordModelSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, pk=None):

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):

        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AllPasswordsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Password.objects.all()
    serializer_class = PasswordModelSerializer
    permission_classes = [IsStaffOrAdmin]
