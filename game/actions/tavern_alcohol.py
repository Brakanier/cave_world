from .functions import *


def alcohol(vk, player, user_ids, peer_id):

    lord = '[id' + str(player.user_id) + '|' + player.nickname + ']'
    mess = '🍺 Всем Эль!!! 🍺\n' + \
           'Лорд по имени ' + lord + ' заказал всем Эль!\n' + \
           'Выше кубки за его успехи и, конечно же, щедрость!\n' + \
           'Пусть все знают его имя!\n' + \
           'У всех в таверне +10 ⚡\n\n'

    for user in user_ids:
        if user > 0:
            mess += '[id' + str(user) + '|🍺]'

    vk.messages.send(
        access_token=token(),
        peer_id=peer_id,
        message=mess,
        random_id=0,
        disable_mentions=0,
    )
