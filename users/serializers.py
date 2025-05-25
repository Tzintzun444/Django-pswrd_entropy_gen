from rest_framework import serializers
from .models import CustomUser


class CustomCustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]

    def update(self, instance, validated_data):

        if 'password' in validated_data:

            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        return super().update(instance, validated_data)


class CustomAdminSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        ]

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        return super().update(instance, validated_data)


# class PatientSerializer(serializers.ModelSerializer):
#     appointments = AppointmentSerializer(many=True, read_only=True)
#     age = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Patient
#         fields = [
#             'id',
#             'first_name',
#             'last_name',
#             'age',
#             'date_of_birth',
#             'contact_number',
#             'email',
#             'address',
#             'medical_history',
#             'appointments'
#         ]
#
#     def validate(self, attrs):
#         if not attrs['email'].endswith('@patient.com'):
#             raise serializers.ValidationError('Email must have the domain: @patient.com')
#
#         return super().validate(attrs)
#
#     def get_age(self, obj):
#         age_td = date.today() - obj.date_of_birth
#         age = age_td.days // 365
#         return f'{age} years old'