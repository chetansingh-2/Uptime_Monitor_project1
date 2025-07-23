from django.contrib import admin

# Register your models here.
from .models import Website, StatusCheck
admin.site.register(Website)
admin.site.register(StatusCheck)
