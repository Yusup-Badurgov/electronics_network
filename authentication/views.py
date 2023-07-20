from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout

from .models import User
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer


class UserRegistrationView(CreateAPIView):
    """ Регистрация пользователя -> Register user """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [~IsAuthenticated] # Только НЕ авторизованные пользователи могут регистрироваться


class LoginViews(APIView):
    """
    Представление для аутентификации пользователя.
    Позволяет выполнить вход пользователя с помощью сериализатора LoginSerializer.
    """

    serializer_class = LoginSerializer
    permission_classes = [~IsAuthenticated]  # Только НЕ авторизованные пользователи могут видеть url авторизации

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для выполнения входа пользователя.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful.'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ Просмотр профиля пользователя -> View user profile """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем queryset профилей, отфильтрованный по текущему имени пользователя
        return User.objects.filter(username=self.request.user)
