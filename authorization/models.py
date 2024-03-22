import uuid

from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager, PermissionsMixin)
# Create your views here.
from django.db import models
# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(username=username, email=self.normalize_email(email)) # используется для создания экземпляра модели пользователей
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='user_photos', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=True,
        null=False, default=AUTH_PROVIDERS.get('email')
    )
    follow = models.ManyToManyField('self', blank=True, related_name='user_follow', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)

    USERNAME_FIELD = 'email' # имейл будет использоваться в качестве уникального идентификатора пользователя при аутентификации
    REQUIRED_FIELDS = ['username'] # какие данные мы будем заполнять при создании суперпользователя


    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



class Hash(models.Model):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)


