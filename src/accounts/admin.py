from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile
from .forms import UserAdminChangeForm, UserAdminCreationForm

class UserProfileAdmin(BaseUserAdmin):
    # form to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'is_staff']
    list_filter = ['is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Add 'password_2' field here
        ('Personal info', {'fields': ('full_name', 'gender', 'profile_pics')})
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    # Remove 'password1' and 'password2' from here
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2'),  # Add 'password_2' field here
        }),
    )

# Register the UserProfileAdmin with your custom model
admin.site.register(UserProfile, UserProfileAdmin)
