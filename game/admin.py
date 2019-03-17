from django.contrib import admin

# Register your models here.
from .models.player import Player
from .models.build import Build, Stock
from .models.war import War
from .models.effects import Effect
from .models.items import Item, ItemChance
from .models.trophy import Trophy, TrophyChance
from .models.chest import Chest, ChestChance
from .models.inventory import Inventory


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


admin.site.register(War)


admin.site.register(Inventory)


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')


@admin.register(Chest)
class ChestAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(ChestChance)
class ChestChanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'chance')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


@admin.register(ItemChance)
class ItemChanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'chance')


@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')


@admin.register(TrophyChance)
class TrophyChanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'chance')
