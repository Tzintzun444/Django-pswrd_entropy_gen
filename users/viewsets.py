from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import CustomCustomerSerializer, CustomAdminSerializer
from .models import CustomUser


class CustomClientViewSet(viewsets.ModelViewSet):

    serializer_class = CustomCustomerSerializer
    queryset = CustomUser.objects.filter(is_staff=False)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        user = serializer.save(is_staff=False, is_superuser=False, role='customer')
        user.set_password(user.password)
        user.save(update_fields=['password'])


class CustomAdminViewSet(viewsets.ModelViewSet):

    serializer_class = CustomAdminSerializer
    queryset = CustomUser.objects.filter(is_staff=True)
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):

        user = serializer.save(is_staff=True, is_superuser=True, role='admin')
        user.set_password(user.password)
        user.save(update_fields=['password'])


# class DoctorViewSet(viewsets.ModelViewSet):
#
#     serializer_class = DoctorSerializer
#     queryset = Doctor.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly, IsDoctor]
#
#     @action(['POST'], detail=True, url_path='set-on-vacation')
#     def set_on_vacation(self, request, pk):
#
#         doctor = self.get_object()
#         doctor.is_on_vacation = True
#         doctor.save()
#
#         return Response({"status": "Doctor is on vacations"})
#
#     @action(['POST'], detail=True, url_path='set-of-vacation')
#     def set_off_vacation(self, request, pk):
#
#         doctor = self.get_object()
#         doctor.is_on_vacation = False
#         doctor.save()
#
#         return Response({"status": "Doctor is not on vacations"})

    # @action(['GET', 'POST', 'DELETE'],
    #         detail=True,
    #         serializer_class=AppointmentSerializer,
    #         url_path='appointments(?:/(?P<appointment_id>[^/.]+))?'
    #         )
    # def appointments(self, request, pk, appointment_id=None):
    #
    #     doctor = self.get_object()
    #
    #     if request.method == 'POST':
    #
    #         data = request.data.copy()
    #         data['doctor'] = doctor
    #         serializer = AppointmentSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     elif request.method == 'GET':
    #
    #         appointments = Appointment.objects.filter(doctor=doctor)
    #         serializer = AppointmentSerializer(appointments, many=True)
    #
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     elif request.method == 'DELETE' and appointment_id:
    #
    #         try:
    #             appointment = Appointment.objects.get(id=appointment_id)
    #             serializer = AppointmentSerializer(appointment)
    #             appointment.delete()
    #
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #
    #         except Appointment.DoesNotExist:
    #
    #             return Response(status=status.HTTP_404_NOT_FOUND)