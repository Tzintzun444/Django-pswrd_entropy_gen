from rest_framework import serializers
from .models import Password
from .utils import Generator


class PasswordGenerationSerializer(serializers.Serializer):

    length = serializers.IntegerField(min_value=1, max_value=30)
    use_uppercase = serializers.BooleanField(default=True, required=False)
    use_numbers = serializers.BooleanField(default=True, required=False)
    use_punctuations = serializers.BooleanField(default=True, required=False)
    custom_characters = serializers.CharField(required=False, allow_blank=True)
    characters_not_allowed = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        password = Generator.generate_password(
            validated_data['length'],
            use_uppercase=validated_data['use_uppercase'],
            use_numbers=validated_data['use_numbers'],
            use_punctuations=validated_data['use_punctuations'],
            customized=validated_data['custom_characters'],
            not_allowed=validated_data['characters_not_allowed']
        )
        entropy = Generator.calculate_entropy(password)
        time_to_decrypt = Generator.calculate_decryption_time(entropy)

        user = self.context['request'].user

        return Password.objects.create(
            user=user,
            password=password,
            entropy=entropy,
            decryption_years_needed=time_to_decrypt
        )


class PasswordModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Password
        fields = [
            'id',
            'user',
            'password',
            'entropy',
            'decryption_years_needed'
        ]
        read_only_fields = [
            'id',
            'user',
            'password',
            'entropy',
            'decryption_years_needed'
        ]
