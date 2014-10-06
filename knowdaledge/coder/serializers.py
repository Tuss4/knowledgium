from rest_framework import serializers


from .models import Coder


class CoderSerializer(serializers.ModelSerializer):

    full_name = serializers.Field(source='get_full_name')

    class Meta:
        model = Coder
        fields = ('id', 'email', 'first_name', 'last_name', 'created', 'full_name')


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password=serializers.CharField()


class RegistrationResponseSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()
