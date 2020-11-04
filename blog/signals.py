from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NotifyMe, Tutorial, BlogPost, ImproveTuto, ImproveTutoComments, Comments
from users.models import Profile
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Tutorial)
def create_tutorial(sender, created, instance, **kwargs):
    title = f"New Tutorial"
    message = f"{instance.user} added a new tutorial"

    my_profile = get_object_or_404(Profile, user=instance.user)
    followers = my_profile.followers.all()

    if created:
        for i in followers:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message, follower_sender=instance.user, tuto_id=instance.id)


@receiver(post_save, sender=BlogPost)
def create_blog(sender, created, instance, **kwargs):
    title = "New Post"
    message = f"{instance.user} added a new blog"

    my_profile = get_object_or_404(Profile, user=instance.user)
    followers = my_profile.followers.all()

    if created:
        for i in followers:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message, follower_sender=instance.user, blog_id=instance.id)


@receiver(post_save, sender=ImproveTuto)
def alert_improvement(sender,created,instance, **kwargs):
    title = "New suggested improvement"
    tutorial_user = instance.tuto.user
    message = f"{instance.user} suggested an improvement for your tutorial {instance.tuto.title }"

    if created:
        NotifyMe.objects.create(user=tutorial_user, notify_title=title, notify_alert=message, follower_sender=instance.user, tuto_id=instance.tuto.id)


@receiver(post_save, sender=Comments)
def alert_tutorial_comment(sender,created,instance,**kwargs):
    title = "New tutorial comment"
    tutorial_user = instance.tutorial.user
    message = f"{instance.user} commented on your tutorial '{instance.tutorial.title}'"

    if created:
        if not instance.user == instance.tutorial.user:
            NotifyMe.objects.create(user=tutorial_user, notify_title=title, notify_alert=message, follower_sender=instance.user, tuto_id=instance.tutorial.id)


@receiver(post_save, sender=ImproveTutoComments)
def alert_tutorial_improvement_comment(sender,created,instance,**kwargs):
    title = "New comment on your improvement "
    tutorial_user = instance.improvetutocomment.user
    message = f"{instance.user} commented on your improvement '{instance.improvetutocomment.title}'"

    if created:
        if not instance.improvetutocomment.user:
            NotifyMe.objects.create(user=tutorial_user, notify_title=title, notify_alert=message, follower_sender=instance.user, improvement_id=instance.improvetutocomment.id)