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

        player = Player.objects.get(user_id=55811116)

        off_send_mess = 'Вы можете отключить рассылку командой "/send off"' + \
                        '\nВключить рассылку можно командой "/send on"'

        vk = self.vk_connect()
        vk.messages.send(
            access_token=self.token(),
            peer_id=player.user_id,
            message=message.text,
            attachment=message.attachment,
            dont_parse_links=1,
            random_id=0
        )
        vk.messages.send(
            access_token=self.token(),
            peer_id=player.user_id,
            message=off_send_mess,
            dont_parse_links=1,
            random_id=0
        )

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
