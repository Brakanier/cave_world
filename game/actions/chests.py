from ..models.chest import Chest, ChestTrophy, ChestItem
from ..models.inventory import InventoryChest, InventoryTrophy
from ..models.build import Stock

from ..actions.functions import *

import random


def get_chest_name(command):
    part = command.split()
    try:
        name = part[1]
    except IndexError:
        return False
    try:
        chest = Chest.objects.get(title__icontains=name)
        return chest
    except Chest.DoesNotExist:
        return False


def add_chest(player, chest):
    try:
        inventory_chest = InventoryChest.objects.get(chest=chest)
        print(inventory_chest)
        InventoryChest.objects.filter(chest=chest).update(count=inventory_chest.count + 1)
        print('Сундук добавлен: ' + str(inventory_chest) + ' +1')
    except InventoryChest.DoesNotExist:
        InventoryChest.objects.create(chest=chest, inventory=player.inventory, count=1)


def remove_chest(player, chest):
    try:
        inventory_chest = InventoryChest.objects.get(chest=chest)
        if inventory_chest.count > 0:
            InventoryChest.objects.filter(chest=chest).update(count=inventory_chest.count - 1)
            print('Сундук удален: ' + str(inventory_chest) + ' -1')
        else:
            print('Ноль сундуков')
    except InventoryChest.DoesNotExist:
        InventoryChest.objects.create(chest=chest, inventory=player.inventory, count=0)
        print('Модель Инвентарь - Сундук создана')


def open_trophy_chest(player, chest):
    inventory_chests = InventoryChest.objects.get(chest=chest, inventory=player.inventory)
    print(inventory_chests)
    message = ''
    if inventory_chests.count > 0:
        remove_chest(player, chest)
        trophy = ChestTrophy.objects.filter(chest=chest)
        rand = random.randint(0, 100)
        for reward in trophy:
            if rand > reward.chance*100:
                if reward.trophy.slug == 'wood':
                    player.build.stock.wood += reward.trophy.value
                    Stock.objects.filter(user_id=player.user_id).update(wood=player.build.stock.wood)
                elif reward.trophy.slug == 'stone':
                    player.build.stock.stone += reward.trophy.value
                    Stock.objects.filter(user_id=player.user_id).update(stone=player.build.stock.stone)
                elif reward.trophy.slug == 'iron':
                    player.build.stock.iron += reward.trophy.value
                    Stock.objects.filter(user_id=player.user_id).update(iron=player.build.stock.iron)
                elif reward.trophy.slug == 'gold':
                    player.build.stock.gold += reward.trophy.value
                    Stock.objects.filter(user_id=player.user_id).update(gold=player.build.stock.gold)
                elif reward.trophy.slug == 'diamond':
                    player.build.stock.diamond += reward.trophy.value
                    Stock.objects.filter(user_id=player.user_id).update(diamond=player.build.stock.diamond)
                print(str(reward.trophy) + ' +' + str(reward.trophy.value))
                message += icon(reward.trophy.slug) + ' ' + str(reward.trophy) + ' +' + str(reward.trophy.value) + '\n'
        if message:
            message = 'Награда с сундука:\n' + message
        else:
            message = 'Сундук оказался пустым!'
    else:
        message = 'У вас нет такого сундука!'
    return message


def get_chests(player):
    chests = InventoryChest.objects.filter(inventory=player.inventory)
    message = ''
    for chest in chests:
        if chest.count > 0:
            message += chest.chest.title + ' - ' + str(chest.count) + ' шт.'
    if not message:
        message = False
    else:
        message = 'Ваши сундуки:\n' + message
    return message


