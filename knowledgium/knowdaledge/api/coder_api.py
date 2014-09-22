from django.contrib.auth import authenticate, login


from coder import serializers as srlzr
from coder.models import Coder
from coder.mixins import CurrentCoderMixin
from coder.permissions import CoderPermission


from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


class CoderDetailView(CurrentCoderMixin, generics.RetrieveUpdateAPIView):

    queryset = Coder.objects.all()
    serializer_class = srlzr.CoderSerializer
    permission_classes = (CoderPermission,)


class RegisterCoderView(views.APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = srlzr.RegisterSerializer(data=request.DATA)

        if serializer.is_valid():

            if not Coder.objects.filter(email=serializer.data.get('email')):
                coder = Coder.objects.create_user(
                    serializer.data.get('email'), password=serializer.data.get('password'),
                    first_name=serializer.data.get('first_name'),
                    last_name=serializer.data.get('last_name'))

                token = Token.objects.create(user=coder)

                result = srlzr.RegistrationResponseSerializer()
                result.data['id'] = coder.pk
                result.data['token'] = token.key

                return Response(result.data, status=status.HTTP_201_CREATED)

            return Response(
                {'detail': 'A coder with that email already exists.'},
                status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginCoderView(views.APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = srlzr.LoginSerializer(data=request.DATA)

        if serializer.is_valid():
            username, password = serializer.data.get('email'), serializer.data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                result = srlzr.RegistrationResponseSerializer()
                result.data['id'] = user.pk
                result.data['token'] = user.auth_token.key

                return Response(result.data, status=status.HTTP_200_OK)

            return Response(
                {'detail': "Invalid credentials provided."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
