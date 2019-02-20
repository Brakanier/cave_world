from django.contrib import admin
from .models import Player, Stock, Build, Forge, Army, War, Crusade

# Register your models here.
# admin.site.register(Player)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nickname', 'lvl', 'first_name', 'last_name')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lvl', 'skull', 'max')


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'forge', 'tavern', 'citadel')


@admin.register(Army)
class ArmyAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'warrior', 'archer', 'wizard')


admin.site.register(Forge)
admin.site.register(War)
admin.site.register(Crusade)



