from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    try:
        user = instance
        user.delete()
    except UserWarning:
        pass


post_save.connect(create_profile, sender=User)
#post_delete.connect(delete_user, sender=Profile)
post_save.connect(update_user, sender=Profile)
