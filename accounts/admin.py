from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login' , 'is_admin')
    list_display_links = (
    'username' ,
    'email'
    )
    fieldsets = ()
    readonly_fields = ('last_login' , 'date_joined' ,'password')
