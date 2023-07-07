from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet, ConnectedBankss
from django.contrib.auth import get_user_model
from django.db import models
from .models import VerifyDocument


@receiver(post_save, sender=get_user_model())
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


