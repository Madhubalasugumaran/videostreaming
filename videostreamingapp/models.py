from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, provider_id, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username, provider_id=provider_id, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, provider_id, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, provider_id, password, **extra_fields)


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

class Video(models.Model):
    name = models.CharField(max_length=100)
    video_url = models.URLField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
