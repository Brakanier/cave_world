from django.contrib import admin
from .models import Player, Stock, Build, Forge, Tavern, Army

# Register your models here.
# admin.site.register(Player)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nickname', 'lvl', 'first_name', 'last_name')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lvl')


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'forge', 'tavern', 'gate')


admin.site.register(Forge)
admin.site.register(Tavern)
admin.site.register(Army)


