from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.models import User


class PasswordField(serializers.CharField):

    def __init__(self, **kwargs): # Переопледеляем инит, что бы пароль отображался в закрытом виде
        kwargs['style'] = {'input_type': 'password'} # Тип ввода пароль
        kwargs.setdefault('write_only', True) # Только для записи, что бы неотображался
        super().__init__(**kwargs)
        self.validators.append(validate_password)
        # Добавляем валидацию пароля (короткий, общеизвестные, из опр. символов)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict: # Делаем проверку на несовпадение паролей
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match '})
        return attrs

    def create(self, validated_data: dict) -> User: # Сохраняем пользователя путем переопределения create
        del validated_data['password_repeat'] # Удаляем поле повтор пароля
        validated_data['password'] = make_password(validated_data['password']) # Добавляем зашифрованный пароль
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email',)

    def create(self, validated_data: dict) -> User:
        user = authenticate(
            username=validated_data['username'],  # Аутентифицируем пользователя по логину паролю
            password=validated_data['password']
        )
        if not user:                              # Если пользователя нет, рейзим ошибку
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password): # Проверяем старый пароль на корректность
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is not  correct')
        return old_password

    def update(self, instance, validated_data): # Переопределяем
        instance.set_password(validated_data['new_password']) # Устанавливаем новый пароль
        instance.save(update_fields=('password',)) # Сохраняем
        return instance
