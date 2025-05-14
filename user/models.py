from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default_pic.png')

    def __str__(self):
        return f'{self.username}'


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tried = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OTP for {self.email} - {self.code}"

    def save(self, *args, **kwargs):
        if self.tried >= 3:
            self.is_expired = True
        super().save(*args, **kwargs)