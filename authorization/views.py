import jwt
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status, permissions
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, EmailVerificationSerializer, LoginSerialiers
from django.conf import settings
from .utils import Util
import os



class CustomRedirect(HttpResponseRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class RegisterEmailView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data) # создание экземляра класса сериализатора
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #

        token = RefreshToken.for_user(user) # создание нового токена доступа для конкретного пользователя
        token_payload = {'email': user.email} # создает словарь, который будет содержать информацию , которая будет добавлена к токену
        token['email'] = user.email  # значение адрес электронной почты
        token['payload'] = token_payload # значение дополнительных данных
        token = str(token.access_token) # преобразует объект токена в строку

        current_site = get_current_site(request).domain  # получение домена нашего сайта, на котором работает приложение
        relative_link = reverse('email-verify') # позволяет получить url адрес
        absurl = 'http://' + current_site + relative_link + "?token=" + token
        email_body = 'Hi ' + ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

        try:
            Util.send_email(data)
        except Exception as e:
            print(f"Failed to send verification email to {user.email}: {e}")
            return Response({'message': 'Failed to send verification email.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        token_payload = {'email': user.email}

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        User = get_user_model()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']) # эти строки декодируют json web token
            user_id = payload['user_id']
            email = payload['email']
            user = User.objects.get(id=user_id, email=email)
            if not user:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return redirect(reverse('login') + f'?email={email}')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except (jwt.exceptions.DecodeError, User.DoesNotExist):
            return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)


            # Create your views here.
class LoginAPIView(APIView):
    serializer_class = LoginSerialiers
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











