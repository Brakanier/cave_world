from django.contrib import admin

from .models import Registration, Chat, Report, Message, FortunePost

# Register your models here.

admin.site.register(Registration)
admin.site.register(Report)
admin.site.register(FortunePost)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('peer_id', 'distribution', 'bones_on', 'alco_on', 'is_admin', 'count_users')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')
