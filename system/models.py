from django.db import models
import random
# Create your models here.


class Registration(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    reg = models.BooleanField(
        default=False,
    )


class Chat(models.Model):
    peer_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    count_users = models.IntegerField(
        default=0,
    )


class Report(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
    )
    user_nickname = models.CharField(
        max_length=30,
    )
    chat_id = models.BigIntegerField(
        db_index=True,
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
    )
    text = models.TextField(
        default='пусто',
    )

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        message = 'ID: ' + str(self.user_id) + \
                  '\nНик: ' + str(self.user_nickname) + \
                  '\nРепорт: ' + 'id-' + str(self.id) + \
                  '\n' + str(self.text)
        vk = self.vk()
        vk.messages.send(
            access_token=self.token(),
            peer_id="55811116",
            message=message,
            random_id=random.getrandbits(31) * random.choice([-1, 1])
        )

    def report(self, player, command, chat_info):
        text = command[7:]
        Report.objects.create(user_id=player.user_id,
                              chat_id=chat_info['peer_id'],
                              user_nickname=player.nickname,
                              text=text,
                              )

        message = 'Репорт отправлен. Администрация ответит в ближайшее время.'
        return message

    def answer_report(self, command, chat_info):
        part = command.split()
        try:
            report = Report.objects.get(id=part[1])
            message = command.replace(part[0] + ' ' + part[1], '')
            if report.user_id == report.chat_id:
                chat_info['chat_id'] = report.chat_id
            else:
                chat_info['chat_id'] = report.chat_id - 2000000000
            chat_info['user_id'] = report.user_id
            chat_info['peer_id'] = report.chat_id
            self.send(self, chat_info, message)
            admin_message = 'Ответ отправлен'
        except Report.DoesNotExist:
            admin_message = 'Репорт не найден'
        return admin_message

    def vk(self):
        import vk_api
        token = '92ea5a422d8e327dbe40934fbeefd4ec722786ce5b63b1db627cc29e2180c45e01dc4eb273910b4b0a30c'
        vk_session = vk_api.VkApi(token=token)
        vk_api = vk_session.get_api()
        return vk_api

    def token(self):
        token = '92ea5a422d8e327dbe40934fbeefd4ec722786ce5b63b1db627cc29e2180c45e01dc4eb273910b4b0a30c'
        return token

    def send(self, chat_info, message):
        vk = self.vk(self)
        if chat_info['user_id'] == chat_info['chat_id']:
            vk.messages.send(
                access_token=self.token(self),
                peer_id=str(chat_info['user_id']),
                message=message,
                random_id=random.getrandbits(31) * random.choice([-1, 1])
            )
        else:
            message = '@id' + str(chat_info['user_id']) + '(' + chat_info['nick'] + ')\n' + message
            vk.messages.send(
                access_token=self.token(self),
                peer_id=str(chat_info['peer_id']),
                chat_id=str(chat_info['chat_id']),
                message=message,
                random_id=random.getrandbits(31) * random.choice([-1, 1])
            )
