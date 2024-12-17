from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Inline admin for Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend UserAdmin to include Profile
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]

# Unregister the default User admin and register the extended one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

