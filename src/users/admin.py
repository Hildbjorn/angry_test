from django.contrib import admin

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'telegram_id',)


admin.site.site_title = 'ЭНГРИ | Тестовое задание | Админка'
admin.site.site_header = 'ЭНГРИ | Тестовое задание | Админка'