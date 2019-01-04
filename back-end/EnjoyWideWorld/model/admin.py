from django.contrib import admin
from model import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Pet)
admin.site.register(models.Position)
admin.site.register(models.Item)
admin.site.register(models.CheckInRecord)
admin.site.register(models.LikeRecord)
admin.site.register(models.BattleRecord)
