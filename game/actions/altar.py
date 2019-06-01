from .constant import *
from .functions import icon, exp_need, get_id

from ..models.player import Player


def altar_info(player):
    player.place = "altar"
    player.save(update_fields=['place'])
    mess = 'Оставьте дары для Хранителя Подземелья!\n' + \
           'Щит - 20' + icon('skull') + '\n' + \
           'Ник - 5' + icon('skull') + '\n' + \
           'Атака - 2' + icon('skull') + '\n' + \
           'Разведка - 5' + icon('skull') + '\n'
    mess += '\nКоманды 💀 Алтаря 💀:\n' + \
            'Алтарь ник - сброс перезарядки ника\n' + \
            'Алтарь щит - добавляет щит на 24ч.\n' + \
            'Алтарь атака - сброс перезарядки атаки\n' + \
            'Алтарь разведка [ID или ссылка на игрока] - даёт полную информацию об игроке\n'

    return mess


def altar(command, player, action_time):
    part = command.split()
    if len(part) < 2:
        mess = 'Команды 💀 Алтаря 💀:\n' + \
               'Алтарь - стоимость\n' + \
               'Алтарь ник - сброс перезарядки ника\n' + \
               'Алтарь щит - добавляет щит на 24ч.\n' + \
               'Алтарь атака - сброс перезарядки атаки\n' + \
               'Алтарь разведка [ID или ссылка на игрока] - даёт полную информацию об игроке\n'
        return mess
    # ЩИТ

    if part[1] == 'щит':
        if player.build.stock.skull >= 20:
            player.build.stock.skull -= 20
            if player.war.shield >= action_time:
                player.war.shield += 24 * 3600
            else:
                player.war.shield = action_time + (24 * 3600)
            player.war.save(update_fields=['shield'])
            player.build.stock.save(update_fields=['skull'])
            mess = 'Хранитель Подземелья наградил вас щитом от нападаний на 24ч.'
        else:
            mess = 'Не хватает черепов - нужно 20' + icon('skull')

        return mess

    # Ник

    elif part[1] == 'ник':
        if player.change_nickname_time <= action_time:
            mess = "Вы и так можете сменить ник!"
        else:
            if player.build.stock.skull >= 5:
                player.build.stock.skull -= 5
                player.change_nickname_time = 0
                player.save(update_fields=['change_nickname_time'])
                player.build.stock.save(update_fields=['skull'])
                mess = 'Хранитель Подземелья позволяет сменить ваше имя!'
            else:
                mess = 'Не хватает черепов - нужно 5' + icon('skull')

        return mess

    # РЕГЕН ЭНЕРГИИ Х2

    elif part[1] == 'энергия':
        return "Скоро..."
        # TODO РЕГЕН ЭНЕРГИИ

    # АТАКА

    elif part[1] == 'атака':
        if player.war.war_last_time + 3600 <= action_time:
            mess = "Вы и так можете атаковать!"
        else:
            if player.build.stock.skull >= 2:
                player.build.stock.skull -= 2
                player.war.war_last_time = 0
                player.save(update_fields=['change_nickname_time'])
                player.war.save(update_fields=['war_last_time'])
                mess = 'Хранитель Подземелья наградил вашу армию силой на еще одно сражение!'
            else:
                mess = 'Не хватает черепов - нужно 2' + icon('skull')

        return mess

    # РАЗВЕДКА

    elif part[1] == 'разведка':
        if len(part) < 3:
            return "Вы не указали игрока!\nАлтарь разведка [ID или ссылка на игрока]"

        if player.build.stock.skull < 5:
            return 'Не хватает черепов - нужно 5' + icon('skull')

        if part[2].isdigit():
            id = int(part[2])
        else:
            id = get_id(part[2])

        try:
            target = Player.objects.select_related('war', 'build', 'build__stock').get(user_id=id)
        except Player.DoesNotExist:
            return "Игрок не найден!"

        player.build.stock.skull -= 5
        player.build.stock.save(update_fields=['skull'])

        # Щит
        if target.war.shield > action_time:
            shield = target.war.shield - action_time
            hour = shield // 3600
            minutes = (shield - (hour * 3600)) // 60
            sec = shield - (minutes * 60) - (hour * 3600)
            shield = str(hour) + ' ч. ' + \
                     str(minutes) + ' м. ' + \
                     str(sec) + ' сек.' + icon('time')
        else:
            shield = 'нет'

        # Склад макс.
        if target.build.stock.lvl >= 30:
            stock_max = target.build.stock.lvl * STOCK_MAX_X30
        else:
            stock_max = target.build.stock.lvl * STOCK_MAX_X

        # Добыча
        stone = 0
        wood = 0
        iron = 0
        diamond = 0
        if target.build.stone_mine_lvl > 0:
            stone = (GET_PASSIVE_STONE + (GET_PASSIVE_STONE_X * target.build.stone_mine_lvl)) // 24
        if target.build.wood_mine_lvl > 0:
            wood = (GET_PASSIVE_WOOD + (GET_PASSIVE_WOOD_X * target.build.wood_mine_lvl)) // 24
        if target.build.iron_mine_lvl > 0:
            iron = (GET_PASSIVE_IRON + (GET_PASSIVE_IRON_X * target.build.iron_mine_lvl)) // 24
        if target.build.diamond_mine_lvl:
            diamond = (GET_PASSIVE_DIAMOND + (GET_PASSIVE_DIAMOND_X * target.build.diamond_mine_lvl)) // 24

        mess = 'Хранитель Подземелья одарил вас Взором Сокола!' + '\n' + \
               'Вы видите владения - ' + '[id' + str(target.user_id) + '|' + target.nickname + ']' + '\n' + \
               'Уровень Лорда: ' + str(target.lvl) + icon('lvl') + '\n' + \
               'Опыт: ' + str(target.exp) + ' / ' + str(exp_need(target.lvl)) + icon('lvl') + '\n' + \
               'Склад: ' + str(target.build.stock.lvl) + ' ур. | ' + str(stock_max) + ' макс.' + '\n' + \
               'Торговый пост: ' + str(target.build.market_lvl) + ' ур.' + '\n' + \
               'Каменоломня: ' + str(target.build.stone_mine_lvl) + ' ур. | ' + str(stone) + ' в час' + '\n' + \
               'Лесопилка: ' + str(target.build.wood_mine_lvl) + ' ур. | ' + str(wood) + ' в час' + '\n' + \
               'Рудник: ' + str(target.build.iron_mine_lvl) + ' ур. | ' + str(iron) + ' в час' + '\n' + \
               'Прииск: ' + str(target.build.diamond_mine_lvl) + ' ур. | ' + str(diamond) + ' в час' + '\n' + \
               'Башня: ' + str(target.build.tower_lvl) + '%' + icon('war') + '\n' + \
               'Стена: ' + str(target.build.wall_lvl) + '%' + icon('shield') + '\n' + \
               'Воины: ' + str(target.war.warrior) + icon('sword') + '\n' + \
               'Лучники: ' + str(target.war.archer) + icon('bow') + '\n' + \
               'Маги: ' + str(target.war.wizard) + icon('orb') + '\n' + \
               'Всего: ' + str(target.war.sum_army()) + icon('war') + '\n' + \
               'Камень: ' + str(target.build.stock.stone) + icon('stone') + '\n' + \
               'Дерево: ' + str(target.build.stock.wood) + icon('wood') + '\n' + \
               'Железо: ' + str(target.build.stock.iron) + icon('iron') + '\n' + \
               'Кристаллы: ' + str(target.build.stock.diamond) + icon('diamond') + '\n' + \
               'Золото: ' + str(target.build.stock.gold) + icon('gold') + '\n' + \
               'Черепа: ' + str(target.build.stock.skull) + icon('skull') + '\n' + \
               'Щит: ' + shield + '\n'

        return mess

    # КАРТА ПЕЩЕР

    elif part[1] == 'пещеры':
        return "Скоро..."
        # TODO КАРТА ПЕЩЕР

    mess = 'Команды 💀 Алтаря 💀:\n' + \
           'Алтарь - стоимость\n' + \
           'Алтарь ник - сброс перезарядки ника\n' + \
           'Алтарь щит - добавляет щит на 24ч.\n' + \
           'Алтарь атака - сброс перезарядки атаки\n' + \
           'Алтарь разведка [ID или ссылка на игрока] - даёт полную информацию об игроке\n'
    return mess

