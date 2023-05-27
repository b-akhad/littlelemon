from django.contrib import admin

# Register your models here.
from .models import Menu
from .models import Booking

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username","email","is_staff","is_active")
    list_filter = ("username","email","is_staff", "is_active")
    fieldsets = (
        (None,{"fields":("username","password")}),
        ("Permissions",{"fields":("email","is_staff","is_active","groups","user_permissions")}),

    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "is_staff",
                "email", "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Menu)