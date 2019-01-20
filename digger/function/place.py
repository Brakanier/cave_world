from .function import *


def mine(vk, player, token):
    if player.place == 'mine':
        message = 'Вы уже в шахте'
    else:
        player.place = 'mine'
        player.save()
        message = 'Вы спустили в шахту'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def cave(vk, player, token):
    if player.place == 'cave':
        message = 'Вы уже в подземелье'
    else:
        player.place = 'cave'
        player.save()
        message = 'Вы вернулись в подземелье'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
