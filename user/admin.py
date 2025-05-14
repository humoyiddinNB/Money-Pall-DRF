from django.contrib import admin

from .models import CustomUser
from .models import EmailOTP

admin.site.register(CustomUser)
admin.site.register(EmailOTP)
