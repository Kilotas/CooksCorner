from django.contrib import admin
from .models import User
from dishes.models import Recipe

admin.site.register(User)
admin.site.register(Recipe)
# Register your models here.
