# apps/users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for a new user, or just save the profile for an existing user.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()