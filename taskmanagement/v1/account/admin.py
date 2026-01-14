from django.contrib import admin

# Register your models here.

from v1.account.models import CustomUser

admin.site.register(CustomUser)