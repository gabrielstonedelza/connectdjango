from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile, LastSeen
from .forms import (UserUpdateForm, ProfileUpdateForm, PasswordChangeForm)
from blog.models import Project, ProjectFiles, ProjectIssues, Issues, NotifyMe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from django.core.paginator import Paginator

from blog.notifications import mynotifications
from blog.process_mail import send_my_mail
import sys


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            useremail = form.cleaned_data.get('email')
            if User.objects.filter(email=useremail).exists():
                messages.warning(request, f"sorry,{useremail} already exists.")
            else:
                form.save()
                username = form.cleaned_data.get('username')
                send_my_mail(f"Welcome to ConnectDjango", settings.EMAIL_HOST_USER,
                             useremail,
                             "Thank you for joining Connect Django,we are happy to see you and we assure you that you will never regret it.<br>Here we help each other by answering posted questions and giving out some tutorials that you and i need to become a better Django developer.<br>Stay blessed and keep on djangoing.<br>Yours sincerely,<br>The ConnectDjango Team.")
                messages.success(request, f'Your account is created {username},login now')
                return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, "users/register.html", context)


@login_required
def profile(request, username):
    my_notify = mynotifications(request.user)
    # myques = Question.objects.filter(question_author=request.user)
    # mytutos = Tutorial.objects.filter(tutorial_author=request.user)

    myprofile = get_object_or_404(Profile, user=request.user)
    following = myprofile.following.all()
    followers = myprofile.followers.all()

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        # "myques": myques,
        # "mytutos": mytutos,
        "following": following,
        "followers": followers,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request, username):
    my_notify = mynotifications(request.user)
    if request.method == "POST":
        uForm = UserUpdateForm(request.POST, instance=request.user)
        pForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if uForm.is_valid() and pForm.is_valid():
            uForm.save()
            pForm.save()
            return redirect('profile', username)
    else:
        uForm = UserUpdateForm(instance=request.user)
        pForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "uform": uForm,
        "pform": pForm,
    }
    if request.is_ajax():
        myprofile = render_to_string("users/edited_profile.html", context, request=request)
        return JsonResponse({
            "form": myprofile
        })
    return render(request, "users/edit_profile.html", context)


@login_required
def user_connection(request, id):
    myprofile = get_object_or_404(Profile, user=request.user)
    following = myprofile.following.all()
    followers = myprofile.followers.all()

    deuser = get_object_or_404(User, id=id)
    message = f"{request.user} started following you"

    if not myprofile.following.filter(id=deuser.id).exists():
        myprofile.following.add(deuser)
        NotifyMe.objects.create(user=deuser, notify_title="Follow Request Notice", notify_alert=message,
                                follower_sender=request.user)

    else:
        myprofile.following.remove(deuser)

    if not deuser.profile.followers.filter(id=request.user.id).exists():
        deuser.profile.followers.add(request.user)
    else:
        deuser.profile.followers.remove(request.user)

    context = {
        "following": following,
        "followers": followers,
        "deuser": deuser,
    }

    if request.is_ajax():
        connection = render_to_string("users/user_connection.html", context, request=request)
        return JsonResponse({
            "results": connection
        })


@login_required
def profile_following(request, id):
    myprofile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, id=id)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    if myprofile.following.filter(id=user.id).exists():
        myprofile.following.remove(user)

        if user.profile.followers.filter(id=request.user.id).exists():
            user.profile.followers.remove(request.user)

    context = {
        "following": following,
        "followers": followers,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
        "user": user,
    }

    if request.is_ajax():
        pconnection = render_to_string("users/profile_connection.html", context, request=request)
        return JsonResponse({
            "results": pconnection
        })


@login_required
def profile_connection_followers(request, id):
    myprofile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, id=id)
    users = User.objects.exclude(id=request.user.id)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    if not myprofile.following.filter(id=user.id).exists():
        myprofile.following.add(user)
        notify_message = f"{request.user} started following you."
        NotifyMe.objects.create(user=user, notify_title="Follow Notice", notify_alert=notify_message,
                                follower_sender=request.user)

    else:
        myprofile.following.remove(user)

    if not user.profile.followers.filter(id=request.user.id).exists():
        user.profile.followers.add(request.user)
    else:
        user.profile.followers.remove(request.user)

    context = {
        "following": following,
        "followers": followers,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
        "user": user,
        "users": users
    }

    if request.is_ajax():
        pconnectionfollowers = render_to_string("users/profile_connection_followers.html", context, request=request)
        return JsonResponse({
            "results": pconnectionfollowers
        })




