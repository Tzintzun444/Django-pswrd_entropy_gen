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
                raise serializers.ValidationError('email', 'The email is already in use')

            current_username = self.instance.username
            new_username = data.get('username')

            if new_username and new_username != current_username and CustomUser.objects.filter(
                    username=new_username).exists():

                raise serializers.ValidationError('username', 'The username is already in use')

        if len(data.get('password')) < 8:
            raise serializers.ValidationError('password', 'Password must have at least 8 characters')

        if data.get('password').isdigit():
            raise serializers.ValidationError('password', 'Password can\'t be only numeric')

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
                raise serializers.ValidationError('email', 'The email is already in use')

            current_username = self.instance.username
            new_username = data.get('username')
            if new_username and new_username != current_username and CustomUser.objects.filter(
                    username=new_username).exists():
                raise serializers.ValidationError('username', 'The username is already in use')

        if len(data.get('password')) < 8:
            raise serializers.ValidationError('password', 'Password must have at least 8 characters')

        if data.get('password').isdigit():
            raise serializers.ValidationError('password', 'Password can\'t be only numeric')

        return super().validate(data)
