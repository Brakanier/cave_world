from .function import *


def mine(player):
    if player.place == 'mine':
        message = 'Вы уже в Шахте'
    else:
        player.place = 'mine'
        player.save()
        message = 'Вы спустили в Шахту'
    send(player=player, message=message)


def cave(player):
    if player.place == 'cave':
        message = 'Вы уже в Подземелье'
    else:
        player.place = 'cave'
        player.save()
        message = 'Вы вернулись в Подземелье'
    send(player=player, message=message)


def land(player):
    if player.place == 'land':
        message = 'Вы уже в Землях'
    else:
        player.place = 'land'
        player.save()
        message = 'Вы вышли в Земли'
    send(player=player, message=message)


def forge(player):
    if player.place == 'forge':
        message = 'Вы уже в Кузнице'
    else:
        player.place = 'forge'
        player.save()
        message = 'Вы зашли в Кузницу'
    send(player=player, message=message)


def tavern(player):
    if player.place == 'tavern':
        message = 'Вы уже в Таверне'
    else:
        player.place = 'tavern'
        player.save()
        message = 'Вы зашли в Таверну!\n' + \
                  'Здесь вы можете нанять воиска.\n' + \
                  'Стоимость:\n' + \
                  '🗡 Воин: ' + str(PRICE_GOLD) + ' ✨ + ' + str(WEAPON) + ' 🗡\n' + \
                  '🏹 Лучник: ' + str(PRICE_GOLD) + ' ✨ + ' + str(WEAPON) + ' 🏹\n' + \
                  '🔮 Маг: ' + str(PRICE_GOLD) + ' ✨ + ' + str(WEAPON) + ' 🔮\n'
    send(player=player, message=message)


def war(player):
    if player.place == 'war':
        message = 'Вы уже в меню Войны'
    else:
        player.place = 'war'
        player.save()
        message = '⚔ Меню войны ⚔\n' + 'Найдите противника и разгромите его!'
    send(player=player, message=message)
