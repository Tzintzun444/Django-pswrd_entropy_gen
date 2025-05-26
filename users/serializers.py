from rest_framework import serializers
from generator.serializers import PasswordModelSerializer
from .models import CustomUser


class CustomCustomerSerializer(serializers.ModelSerializer):

    passwords = PasswordModelSerializer(many=True, read_only=True)

    class Meta:

        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'passwords'
        ]

    def update(self, instance, validated_data):

        if 'password' in validated_data:

            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        return super().update(instance, validated_data)

    def validate(self, data):

        if self.instance:

            current_email = self.instance.email
            new_email = data.get('email')

            if new_email and CustomUser.objects.filter(email=new_email).exists() and current_email != new_email:
                raise serializers.ValidationError('The email is already in use')

            current_username = self.instance.username
            new_username = data.get('username')

            if new_username and new_username != current_username and CustomUser.objects.filter(
                    username=new_username).exists():

                raise serializers.ValidationError('The username is already in use')

        if len(data.get('password')) < 8:
            raise serializers.ValidationError('Password must have at least 8 characters')

        return super().validate(data)


class CustomAdminSerializer(serializers.ModelSerializer):

    passwords = PasswordModelSerializer(many=True, read_only=True)

    class Meta:

        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'passwords'
        ]

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        return super().update(instance, validated_data)

    def validate(self, data):

        if self.instance:

            current_email = self.instance.email
            new_email = data.get('email')

            if new_email and CustomUser.objects.filter(email=new_email).exists() and current_email != new_email:
                raise serializers.ValidationError('The email is already in use')

            current_username = self.instance.username
            new_username = data.get('username')

            if new_username and new_username != current_username and CustomUser.objects.filter(
                    username=new_username).exists():
                raise serializers.ValidationError('The username is already in use')

        if len(data.get('password')) < 8:
            raise serializers.ValidationError('Password must have at least 8 characters')

        return super().validate(data)

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
