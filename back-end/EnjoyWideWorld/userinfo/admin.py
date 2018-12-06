from django.contrib import admin
from userinfo import models

# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Pet)
admin.site.register(models.Position)