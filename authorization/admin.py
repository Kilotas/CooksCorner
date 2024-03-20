from django.contrib import admin
from .models import User
from dishes.models import Recipe, Like

admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Like)
# Register your models here.
