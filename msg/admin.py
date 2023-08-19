from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User


# Juntar profile com user no admin
class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

