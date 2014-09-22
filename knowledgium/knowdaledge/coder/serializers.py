from rest_framework import serializers


from .models import Coder


class CoderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coder
        fields = ('id', 'email', 'first_name', 'last_name', 'created')


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
