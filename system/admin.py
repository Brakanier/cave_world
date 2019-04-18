from django.contrib import admin

from .models import Registration, Chat

# Register your models here.

admin.site.register(Registration)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('peer_id', 'count_users')

