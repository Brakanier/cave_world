from .function import *


def dig(vk, player, action_time, token):
    need_energy = 1
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        player.energy = player.energy - need_energy
        player.stock.stone = player.stock.stone + 2
        player.stock.save()
        player.save()
        message = 'Добыто: Камень 2шт.'
    else:
        message = 'Недостаточно энергии'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
