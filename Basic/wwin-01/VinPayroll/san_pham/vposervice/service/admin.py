from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission

from django.contrib import admin
admin.site.register(Permission)

# Register your models here.
admin.site.register(Claim)
