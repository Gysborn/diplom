from django.contrib.auth import login, logout
from rest_framework import generics, permissions
from rest_framework.response import Response

from core.serialisers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignUpView(generics.CreateAPIView): # Ручка на регистрацию
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView): # Ручка на вход
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data) # Сериализируем данные из запроса
        serializer.is_valid(raise_exception=True) # Проверяем на корректность иначе рейзим ошибку
        login(request=request, user=serializer.save()) # Логиним пользователя
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self): # Переопределяем метод
        return self.request.user # Будет возвращать объект по user

    def perform_destroy(self, instance): # Переопределяем метод
        logout(self.request) # Вызываем logout не удаляя экземпляр ...


class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
