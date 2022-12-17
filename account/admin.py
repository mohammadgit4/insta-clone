from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def phone_number(obj):
        if not (obj.country_code and obj.phone_no):
            return ''
        else:
            return f'+{obj.country_code} {obj.phone_no}'
    list_display = ('id', 'username', 'full_name', 'email', 'gender', 'date_of_birth', phone_number, 'is_staff', 'is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        ('Credentials', {'fields': ('email', 'username', 'country_code', 'phone_no', 'password')}),
        ('Personal info', {'fields': ('profile', 'gender', 'full_name', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'otp', 'tfa')}),
    )
    add_fieldsets = (
        ('Add New User.', {
            'classes': ('wide',),
            'fields': ('email', 'country_code', 'phone_no', 'username', 'full_name', 'password1', 'password2', 'is_staff'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()