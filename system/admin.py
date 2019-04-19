from django.contrib import admin

from .models import Registration, Chat, Report

# Register your models here.

admin.site.register(Registration)
admin.site.register(Report)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('peer_id', 'count_users')

