from django.contrib import admin
from django import forms

from .models import User, Account, SavingsGroup, Piggybox, Address
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


# Register your models here.
admin.site.register(Address)
admin.site.register(SavingsGroup)
admin.site.register(Piggybox)
# admin.site.register(models.User)


class SavingsGroupInline(admin.TabularInline):  # or admin.StackedInline
    model = SavingsGroup.group_members.through
    extra = 1  # Number of empty forms to display

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'transaction_pin': forms.PasswordInput(render_value=True),
        }

@admin.register(User)
class CustomAdmin(UserAdmin):
   
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
 
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
            }
 
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
 
        return form
    
    add_form = CustomUserCreationForm
    list_display = ('email', 'firstname')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firstname', 'lastname', 'email', 'phone_code', 'phone', 'address', 'transaction_pin', 'password1', 'password2',), # password1 & 2 are default for the UserAdmin class
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ()
    fieldsets = ()
    readonly_fields = [
        'date_joined', 'last_login'
    ]

    inlines = [SavingsGroupInline]  # Add the inline class here


admin.site.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     readonly_fields = ('username', 'account_number','account_balance', 'pin' )


admin.register(Piggybox)
class PiggyboxCustomAdmin:
    readonly_fields = [
        'interest', 'date_created', 'date_break', 'date_fulfilled'
    ]

admin.register(PiggyboxCustomAdmin)

