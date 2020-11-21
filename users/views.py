from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile
from .forms import (UserUpdateForm, ProfileUpdateForm, PasswordChangeForm)
from blog.models import NotifyMe
from django.core.paginator import Paginator
from blog.notifications import mynotifications
from blog.process_mail import send_my_mail
from blog.models import ChatRoom,Blog

def register(request):
    username = ''
    useremail = ''
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            useremail = form.cleaned_data.get('email')
            if User.objects.filter(email=useremail).exists():
                messages.warning(request, f"sorry,{useremail} already exists.")
            else:
                form.save()
                username = form.cleaned_data.get('username')
                send_my_mail(f"Welcome to ConnectDjango {username}", settings.EMAIL_HOST_USER, useremail, {"name":username}, "email_templates/success.html")
                messages.success(request, f'Your account is created {username},login now')
                return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        "name": username
    }
    

    return render(request, "users/register.html", context)


@login_required
def profile(request, username):
    my_notify = mynotifications(request.user)

    myprofile = get_object_or_404(Profile, user=request.user)
    blogs = Blog.objects.filter(user=request.user).order_by('-date_posted')
    blog_count = blogs.count()

    paginator = Paginator(blogs, 15)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    following = myprofile.following.all()
    followers = myprofile.followers.all()


    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "following": following,
        "followers": followers,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
        "blogs": blogs,
        "blog_count": blog_count
    }
    return render(request, "users/profile.html", context)


@login_required
def profile_followings(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)
    my_notify = mynotifications(request.user)

    following = myprofile.following.all()
    paginator = Paginator(following, 15)
    page = request.GET.get('page')
    following = paginator.get_page(page)

    context = {
        "following": following,
        "myprofile": myprofile,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "users/profile_followings.html", context)


@login_required
def profile_followers(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)
    my_notify = mynotifications(request.user)

    followers = myprofile.followers.all()
    paginator = Paginator(followers, 15)
    page = request.GET.get('page')
    followers = paginator.get_page(page)

    context = {
        "myprofile": myprofile,
        "followers": followers,
        "following_count": myprofile.my_following_count(),
        "followers_count": myprofile.my_followers_count(),
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "users/profile_followers.html", context)


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

    df_count = deuser.profile.following.all().count
    dfs_count = deuser.profile.followers.all().count

    deuser_following = deuser.profile.following.all()
    deuser_followers = deuser.profile.followers.all()

    if not myprofile.following.filter(id=deuser.id).exists():
        myprofile.following.add(deuser)
        NotifyMe.objects.create(user=deuser, notify_title="Follow Request Notice", notify_alert=message, follower_sender=request.user)

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
        "defollowing": deuser_following,
        "defollowers": deuser_followers,
        "df_count": df_count,
        "dfs_count": dfs_count,
    }

    if request.is_ajax():
        connection = render_to_string("users/user_connection.html", context, request=request)
        return JsonResponse({
            "results": connection
        })


