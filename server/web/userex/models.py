from django.db.models import signals
from django.dispatch import receiver
import linux_user
from django.contrib.auth.models import User


@receiver(signals.post_init)
def create_user_callback(sender, **kwargs):
    if sender == User:
        if 'instance' in kwargs:
            linux_user.register_user(kwargs['instance'].username)
