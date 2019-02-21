from django.core.management.base import BaseCommand
from time import sleep


class Command(BaseCommand):
    # Задаём текст помощи, который будет
    # отображён при выполнении команды
    # python manage.py createtags --help
    help = 'Creates specified number of tags'

    def add_arguments(self, seconds):
        # Указываем сколько и каких аргументов принимает команда.
        # В данном случае, это один аргумент типа int.
        seconds.add_argument('seconds', nargs=1, type=int)

    def handle(self, *args, **options):
        while(True):
            self.stdout.write('Unsleep')
            sleep(options['seconds'][0])
