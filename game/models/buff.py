from django.db import models


class Buff(models.Model):
    player = models.ForeignKey(
        'game.Player',
        on_delete=models.SET(None),
        null=True,
        related_name='buffs',
    )
    buff_type = models.CharField(
        max_length=30,
        db_index=True,
    )
    time_end = models.BigIntegerField(
        default=0,
    )

    def buff_check(self, action_time):
        if action_time > self.time_end:
            self.delete()
            return False
        else:
            return True
