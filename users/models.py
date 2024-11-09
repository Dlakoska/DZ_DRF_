from django.contrib.auth.models import AbstractUser

from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=12, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=30, verbose_name="Город", **NULLABLE)
    image = models.ImageField(
        upload_to="users/media/avatars", **NULLABLE, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
