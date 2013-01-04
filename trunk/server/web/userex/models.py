from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
import linux_user


@receiver(signals.post_save)
def create_user_callback(sender, **kwargs):
    if sender == User:
        if 'created' in kwargs and kwargs['created'] and 'instance' in kwargs:
            print('\x1b[42m' + '-' * 15 + ' user for ' + kwargs['instance'].username +
                ' should be created here ' + '-' * 15 + '\x1b[0m')
            linux_user.register_user(kwargs['instance'].username)
