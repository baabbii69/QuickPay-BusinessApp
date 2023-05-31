from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet
from django.contrib.auth import get_user_model
from django.db import models
from .models import VerifyDocument


@receiver(post_save, sender=get_user_model())
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


# @receiver(post_save, sender=VerifyDocument)
# def create_utility(sender, instance, created, **kwargs):
#     if created and instance.is_utility:
#         Utility.objects.create(user=str(instance.user.id), name=instance.legal_BN)


# @receiver(post_save, sender=VerifyDocument)
# def create_utility(sender, instance, created, **kwargs):
#     if created and instance.is_utility and instance.is_flexible == False:
#         Utility.objects.create(user=str(instance.user.id))

# @receiver(post_save, sender=BillType)
# def add_bill_type_to_utility(sender, instance, created, **kwargs):
#     if created:
#         user_id = instance.user_id  # Assuming BillType has a foreign key field `user` representing the current user
#         utility_instance = Utility.objects.get(user_id=user_id)
#         utility_instance.bill_types.add(instance)
