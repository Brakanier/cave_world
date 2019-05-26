
def altar(command, player, action_time):
    part = command.split()
    if part[1] == 'щит':
        if player.build.stock.skull >= 10:
            player.build.stock.skull -= 10
            player.war.shield += 24 * 3600
            player.war.save(update_fields=['shield'])
            player.build.stock.save(update_fields=['skull'])
            mess = 'Добавлен щит на 24 ч.'
        else:
            mess = 'У вас не хватает черепов!'
    elif part[1] == 'ник':
        if player.change_nickname_time <= action_time:
            mess = "Вы и так можете сменить ник!"
        else:
            if player.build.stock.skull >= 10:
                player.build.stock.skull -= 10
                player.change_nickname_time = 0
                player.save(update_fields=['change_nickname_time'])
                player.build.stock.save(update_fields=['skull'])
                mess = 'Вы теперь можете сменить ник!'
            else:
                mess = 'У вас не хватает черепов!'
    elif part[1] == 'энергия':
        pass
        # TODO РЕГЕН ЭНЕРГИИ
    elif part[1] == 'атака':
        if player.war.war_last_time + 3600 <= action_time:
            mess = "Вы и так можете атаковать!"
        else:
            if player.build.stock.skull >= 2:
                player.build.stock.skull -= 2
                player.war.war_last_time = 0
                player.save(update_fields=['change_nickname_time'])
                player.war.save(update_fields=['war_last_time'])
                mess = 'Вы теперь можете атаковать!'
            else:
                mess = 'У вас не хватает черепов!'
    elif part[1] == 'разведка':
        pass
        # TODO РАЗВЕДКА
    elif part[1] == 'пещеры':
        pass
        # TODO КАРТА ПЕЩЕР
