from django.contrib import admin
from django.utils.html import format_html

from .models import Account, Profile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_admin')
    list_display_links = (
        'username',
        'email'
    )
    fieldsets = ()
    readonly_fields = ('last_login', 'date_joined', 'password')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html('<img src="{}" width="30" style="border-radius:100%;">'.format(obj.picture.url))

    thumbnail.short_description = 'Picture'

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    list_display_links = (
        'user',
    )
