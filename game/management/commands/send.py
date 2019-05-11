from django.core.management.base import BaseCommand, CommandError
from ...models.player import Player
from system.models import Chat, Message

import vk_api
import time


class Command(BaseCommand):
    help = 'Send message for all users and chats'

    def add_arguments(self, parser):
        parser.add_argument(type=int, dest='id')

    def handle(self, *args, **options):
        self.stdout.write('Start sending')
        try:
            message = Message.objects.get(pk=options['id'])
        except Message.DoesNotExist:
            raise CommandError('Message "%s" does not exist' % options['id'])
        chats = Chat.objects.values_list('peer_id').all()
        chat_errors = 0
        vk = self.vk_connect()
        for chat_peer in chats:
            try:
                vk.messages.send(
                    access_token=self.token(),
                    peer_id=chat_peer[0],
                    message=message.text,
                    random_id=0
                )
                self.stdout.write('OK - ' + str(chat_peer[0]))
            except:
                chat_errors += 1
                self.stdout.write('FAIL - ' + str(chat_peer[0]))
            time.sleep(1)

        self.stdout.write('Chat Errors - ' + str(chat_errors))

        players = Player.objects.filter(lvl__gt=1).values_list('user_id').all()
        parts = self.explode(players, 100)
        for part in parts:
            peer_ids = "1"
            for user in part:
                peer_ids += ',' + str(user[0])
            try:
                vk.messages.send(
                    access_token=self.token(),
                    peer_ids=peer_ids,
                    message=message.text,
                    random_id=0
                )
                self.stdout.write('OK')
            except:
                self.stdout.write('FAIL')
            self.stdout.write('Users Send - ' + str(len(part) / len(players) * 100) + ' %')
            time.sleep(1)

        self.stdout.write('End sending')


    @staticmethod
    def explode(lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    def token(self):
        return '92ea5a422d8e327dbe40934fbeefd4ec722786ce5b63b1db627cc29e2180c45e01dc4eb273910b4b0a30c'

    def vk_connect(self):
        vk_session = vk_api.VkApi(token=self.token())
        vk = vk_session.get_api()
        return vk

