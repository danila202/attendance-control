from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Group, Subscription


@receiver(post_save, sender=Subscription)
@receiver(post_delete, sender=Subscription)
def update_children_count(sender, instance, **kwargs):
    group = instance.group
    group.children_count = group.subscriptions.values('child').distinct().count()
    group.save()


@receiver(pre_save, sender=Subscription)
def calculate_discounted_price(sender, instance, **kwargs):
    if instance.sale:
        instance.price_with_sale = instance.subscription_type.price - instance.sale.price
    else:
        instance.price_with_sale = instance.subscription_type.price

