from ..models.chest import Chest, ChestTrophy, ChestItem
from ..models.inventory import InventoryChest, InventoryTrophy
from ..models.build import Stock

from ..actions.functions import *

import random


def get_chest_object(command):
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


def get_chest(slug):
    return Chest.objects.get(slug=slug)


def add_chest(player, chest, count=1):
    try:
        inventory_chest = player.inventory.chests.get(chest=chest)
        print(inventory_chest)
        player.inventory.chests.filter(chest=chest).update(count=inventory_chest.count + count)
        print('Сундук добавлен: ' + str(inventory_chest) + ' +1')
    except InventoryChest.DoesNotExist:
        player.inventory.chests.create(chest=chest, inventory=player.inventory, count=count)


def remove_chest(player, chest):
    try:
        inventory_chest = player.inventory.chests.get(chest=chest)
        if inventory_chest.count > 0:
            player.inventory.chests.filter(chest=chest).update(count=inventory_chest.count - 1)
            print('Сундук удален: ' + str(inventory_chest) + ' -1')
        else:
            print('Ноль сундуков')
    except InventoryChest.DoesNotExist:
        player.inventory.chests.create(chest=chest, inventory=player.inventory, count=0)
        print('Модель Инвентарь - Сундук создана')


def get_chest_mine(player, message):
    chest_rand = random.randint(0, 100)
    chest = get_chest('mine_chest')
    if chest_rand >= (100 - chest.chance_for_get):
        add_chest(player, chest)
        message += '\nВы нашли Шахтерский Сундук!'
    return message


def open_trophy_chest(player, chest):
    try:
        inventory_chest = player.inventory.chests.get(chest=chest)
    except InventoryChest.DoesNotExist:
        player.inventory.chests.create(chest=chest, inventory=player.inventory, count=0)
        return 'У вас нет такого сундука!'
    message = ''
    if inventory_chest.count > 0:
        remove_chest(player, chest)
        trophy = inventory_chest.chest.trophy_chance.all()
        rand = random.randint(0, 100)
        for reward in trophy:
            if reward.chance*100 >= rand:
                if reward.trophy.slug == 'wood':
                    player.build.stock.wood += reward.trophy.value
                elif reward.trophy.slug == 'stone':
                    player.build.stock.stone += reward.trophy.value
                elif reward.trophy.slug == 'iron':
                    player.build.stock.iron += reward.trophy.value
                elif reward.trophy.slug == 'gold':
                    player.build.stock.gold += reward.trophy.value
                elif reward.trophy.slug == 'diamond':
                    player.build.stock.diamond += reward.trophy.value
                print(str(reward.trophy) + ' +' + str(reward.trophy.value))
                message += icon(reward.trophy.slug) + ' ' + str(reward.trophy) + ' +' + str(reward.trophy.value) + '\n'
        player.build.stock.save(update_fields=['wood', 'stone', 'iron', 'diamond', 'gold'])
        if message:
            message = 'Награда с сундука:\n' + message
        else:
            message = 'Сундук оказался пустым!'
        message = 'Вы открыли - ' + str(chest.title) + '\n' + message
    else:
        message = 'У вас нет такого сундука!'
    return message


def get_chests(player):
    chests = player.inventory.chests.all()
    message = ''
    for chest in chests:
        if chest.count > 0:
            message += chest.chest.title + ' - ' + str(chest.count) + ' шт.\n'
    if not message:
        message = False
    else:
        message = 'Ваши сундуки:\n' + message
    return message


