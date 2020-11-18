from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NotifyMe, Message, PrivateMessage,ChatRoom
from users.models import Profile
from django.shortcuts import get_object_or_404


