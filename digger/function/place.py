from .function import *


def mine(vk, player, token):
    if player.place == 'mine':
        message = 'Вы уже в Шахте'
    else:
        player.place = 'mine'
        player.save()
        message = 'Вы спустили в Шахту'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def cave(vk, player, token):
    if player.place == 'cave':
        message = 'Вы уже в Подземелье'
    else:
        player.place = 'cave'
        player.save()
        message = 'Вы вернулись в Подземелье'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def forge(vk, player, token):
    if player.place == 'forge':
        message = 'Вы уже в Кузнице'
    else:
        player.place = 'forge'
        player.save()
        message = 'Вы зашли в Кузницу'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
