from system.models import FortunePost
from ..actions.functions import *
from ..actions.chests import *
import random


def write(data):
    f = open('text.txt', 'w')
    f.write(data)
    f.close()


class Fortune:

    def __init__(self, player, comment):
        try:
            self.fortune_post = FortunePost.objects.get(post_id=comment['post_id'])
        except FortunePost.DoesNotExist:
            self.fortune_post = None

        self.post_id = comment['post_id']
        self.player = player
        self.comment = comment
        self.reward_choice = (
            'skull',
            'energy',
            'chest',
            'gold'
        )
        self.reward_icon = {
            'skull': '💀',
            'energy': '⚡',
            'chest': '🎁',
            'gold': '✨',
        }

    def fortune(self):
        if self.fortune_post:
            if self.check_coin():
                self.player.fortune_coin -= 1
                reward = (
                    random.choice(self.reward_choice),
                    random.choice(self.reward_choice),
                    random.choice(self.reward_choice),
                )
                ic = (
                    self.reward_icon[reward[0]],
                    self.reward_icon[reward[1]],
                    self.reward_icon[reward[2]],
                )
                if reward[0] == reward[1] == reward[2]:
                    if 'skull' in reward:
                        self.player.build.stock.skull += 10
                        self.player.build.stock.save(update_fields=['skull'])
                        reward_mess = '🎉 Вы выиграли 10 черепов! 🎉\n'
                    elif 'gold' in reward:
                        self.player.build.stock.gold += 1000
                        self.player.build.stock.save(update_fields=['gold'])
                        reward_mess = '🎉 Вы выиграли 1000 золота! 🎉\n'
                    elif 'energy' in reward:
                        self.player = energy(self.player, self.comment['date'])
                        self.player.energy += 30
                        reward_mess = '🎉 Вы выиграли 30 энергии! 🎉\n'
                    elif 'chest' in reward:
                        chest = Chest.objects.get(slug='present_chest')
                        add_chest(self.player, chest, 5)
                        reward_mess = '🎉 Вы выйграли 5 Подарочных Сундуков! 🎉\n'

                else:
                    reward_mess = 'Где ваша удача?\n'

                self.player.save(update_fields=['fortune_coin', 'fortune_time', 'energy'])
                coin_mess = 'Монет осталось: ' + str(self.player.fortune_coin) + ' 🧿'
                mess = self.create_mess(ic)
                mess += '\n\n' + reward_mess + coin_mess
            else:
                mess = 'У вас нет 🧿 Монет Фортуны 🧿'
            try:
                send_comment(self.comment['post_id'], self.comment['id'], mess)
            except:
                pass

    def create_mess(self, ic):
        head = '\n╔═════════╗\n' + \
               '║۞ Fortune ۞ ║\n'
        mess = '╠===╦===╦===╣\n' + \
               '║ ' + ic[0] + '║ ' + ic[1] + '║ ' + ic[2] + '║\n' + \
               '╚===╩===╩===╝'
        mess = head + mess
        return mess

    def check_coin(self):
        coins(self.player, self.comment['date'])
        if self.player.fortune_coin > 0:
            return True
        else:
            return False

