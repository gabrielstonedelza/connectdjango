from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile, Group, GroupPost, LoginConfirmCode, GroupAdminMsg, LastSeen, Comments
from .forms import (UserUpdateForm, ProfileUpdateForm, GroupUpdateForm, GroupPostForm, CreateNewGroupForm, AdminMessageForm, CommentsForm, PasswordChangeForm)
from blog.models import Question, Tutorial, NotifyMe
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
                             useremail, "Thank you for joining Connect Django,we are happy to see you and we assure you that you will never regret it.<br>Here we help each other by answering posted questions and giving out some tutorials that you and i need to become a better Django developer.<br>Stay blessed and keep on djangoing.<br>Yours sincerely,<br>The ConnectDjango Team.")
                messages.success(request, f'Your account is created {username},login now')
                return redirect('login')

    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, "users/register.html", context)


def logout_request(request):
    try:
        ul1 = LoginConfirmCode.objects.filter(logged_user=request.user)
        if ul1:
            ul1.delete()
        #     save users last seen
        LastSeen.objects.create(user=request.user)

    except LookupError as e:
        messages.info(request, f"User details relating to your information does not exist,{e}")
    return render(request, "blog/logout.html")


@login_required
def profile(request, username):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)
        myques = Question.objects.filter(question_author=request.user)
        mytutos = Tutorial.objects.filter(tutorial_author=request.user)

        myprofile = get_object_or_404(Profile, user=request.user)
        following = myprofile.following.all()
        followers = myprofile.followers.all()

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "myques": myques,
        "mytutos": mytutos,
        "following": following,
        "followers": followers,
        "following_count": myprofile.myfollowing_count(),
        "followers_count": myprofile.myfollowers_count(),
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request, username):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
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
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

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
        "following_count": myprofile.myfollowing_count(),
        "followers_count": myprofile.myfollowers_count(),
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
        NotifyMe.objects.create(user=user, notify_title="Follow Notice", notify_alert=notify_message, follower_sender=request.user)

    else:
        myprofile.following.remove(user)

    if not user.profile.followers.filter(id=request.user.id).exists():
        user.profile.followers.add(request.user)
    else:
        user.profile.followers.remove(request.user)

    context = {
        "following": following,
        "followers": followers,
        "following_count": myprofile.myfollowing_count(),
        "followers_count": myprofile.myfollowers_count(),
        "user": user,
        "users": users
    }

    if request.is_ajax():
        pconnectionfollowers = render_to_string("users/profile_connection_followers.html", context, request=request)
        return JsonResponse({
            "results": pconnectionfollowers
        })


@login_required
def all_groups(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)
        groups = Group.objects.all().order_by('-date_created')

        paginator = Paginator(groups, 8)
        page = request.GET.get('page')
        groups = paginator.get_page(page)

        user_group_limit = 1
        can_create_group = False
        uu = Group.objects.filter(group_leader=request.user)

        user = request.user

        if uu.count() < user_group_limit:
            can_create_group = True
        else:
            can_create_group = False

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "groups": groups,
        "can_create_group": can_create_group,
        "user": user,
    }

    return render(request, "users/all_groups.html", context)


class CreateNewGroupView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['group_name', 'logo', 'group_description']
    success_url = '/groups'

    def form_valid(self, form):
        form.instance.group_leader = self.request.user
        return super().form_valid(form)


@login_required
def group_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)
        group = get_object_or_404(Group, id=id)
        mymembers = group.members.all()
        members_email = []
        for i in mymembers:
            members_email.append(i.email)

        my_group_posts = GroupPost.objects.filter(group=group).order_by('-date_posted')
        admin_notes_all = GroupAdminMsg.objects.all().order_by('-date_sent')

        # new group post form
        if request.method == "POST":
            form = GroupPostForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                photo = form.cleaned_data.get('photo')
                GroupPost.objects.create(group=group, gmember=request.user, title=title, content=content, photo=photo)
                for i in mymembers:
                    NotifyMe.objects.create(user=i, notify_title="New Group Post", notify_alert=f"{request.user} posted to {group}", follower_sender=request.user, gname=group)
                send_my_mail(f"{request.user.username} posted in your group", settings.EMAIL_HOST_USER, members_email,
                             f"{request.user.username} just made a post to the group {group.group_name}. \n You are joining this group and you would be notified anytime a member makes a post to the group.")
                return redirect('group_posts')
        else:
            form = GroupPostForm()

        # admin notes form
        if request.method == "POST":
            ad_form = AdminMessageForm(request.POST)
            if ad_form.is_valid():
                message = ad_form.cleaned_data.get('message')
                if group.group_leader == request.user:
                    GroupAdminMsg.objects.create(g_leader=request.user, message=message)
                    for i in mymembers:
                        NotifyMe.objects.create(user=i, notify_title="Admin Messages",
                                                notify_alert=f"New Message from Group Admin", follower_sender=request.user,
                                                gname=group)
                    send_my_mail(f"New message from admin", settings.EMAIL_HOST_USER, members_email, f"{group.group_name}'s admin has send you a message,login into your account and read message.")
                    messages.success(request, f"Message has been sent to all members")
                    return redirect('group_detail', id)
        else:
            ad_form = AdminMessageForm()

        if group:
            group.views += 1
            group.save()

        somemembers = {}
        for i in mymembers:
            if i not in somemembers:
                somemembers[i] = i

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "form": form,
        "ad_form": ad_form,
        "group": group,
        "somemembers": somemembers,
        "my_group_posts": my_group_posts,
        "mymembers": mymembers,
        "admin_notes_all": admin_notes_all,
    }

    return render(request, "users/group_detail.html", context)


@login_required
def group_update(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)
        users = User.objects.exclude(id=request.user.id)

        group = get_object_or_404(Group, group_leader=request.user)
        if request.method == "POST":
            form = GroupUpdateForm(request.POST, request.FILES, instance=group)
            if form.is_valid():
                form.save()
        else:
            form = GroupUpdateForm(instance=group)
        group = get_object_or_404(Group, group_leader=request.user)
        gmembers = group.members.all()
        pending_list = group.pending_list.all()

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "form": form,
        "users": users,
        "gmembers": gmembers,
        "group": group,
        "pending_list": pending_list,
    }
    return render(request, "users/edit_group.html", context)


@login_required
def remove_member(request, id):
    group = get_object_or_404(Group, group_leader=request.user)
    gmembers = group.members.all()
    user = get_object_or_404(User, id=id)
    users = User.objects.exclude(id=request.user.id)

    if group.members.filter(id=user.id).exists():
        group.members.remove(user)

    context = {
        "user": user,
        "gmembers": gmembers,
        "users": users,
    }

    if request.is_ajax():
        user_out = render_to_string("users/remove_member.html", context, request=request)
        return JsonResponse({
            "form": user_out
        })


@login_required
def join_group(request, id):
    group = get_object_or_404(Group, id=id)
    gmembers = group.members.all()
    gpmembers = group.pending_list.all()

    user = request.user

    if not group.members.filter(id=user.id).exists() and not group.pending_list.filter(id=user.id).exists():
        group.pending_list.add(user)
        notify_message = f"{user.username} has requested to join your group."
        NotifyMe.objects.create(user=group.group_leader, notify_title="New Group Request", notify_alert=notify_message, follower_sender=request.user, gname=group)

    else:
        group.members.remove(user)

    context = {
        "group": group,
        "user": user,
        "gmembers": gmembers,
        "gpmembers": gpmembers,
    }

    if request.is_ajax():
        joingroup = render_to_string("users/join_group.html", context, request=request)
        return JsonResponse({"form": joingroup})


@login_required
def add_pending_members(request, id):
    group = get_object_or_404(Group, group_leader=request.user)
    gmembers = group.members.all()
    user = get_object_or_404(User, id=id)
    users = User.objects.exclude(id=request.user.id)
    pending_list = group.pending_list.all()

    if not group.members.filter(id=user.id).exists():
        group.members.add(user)
        group.pending_list.remove(user)
        notify_message = f"Hi {user.username}, {group.group_name} added you to their group."
        NotifyMe.objects.create(user=user, notify_title="Group Member Active", notify_alert=notify_message, follower_sender=group.group_leader, gname=group)

    context = {
        "user": user,
        "group": group,
        "pending_list": pending_list,
        "users": users,
    }

    if request.is_ajax():
        add_pending_member = render_to_string("users/add_pending_members.html", context, request=request)
        return JsonResponse({"form": add_pending_member})


@login_required
def group_post_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)
        has_liked = False

        post = GroupPost.objects.get(id=id)
        message = f"{request.user.username} commented on your post '{post.title}'"
        if post.likes.filter(id=request.user.id).exists():
            has_liked = True

        if post:
            post.views += 1
            post.save()
        comments = Comments.objects.filter(post=post).order_by('-date_posted')
        comments_count = comments.count()

        paginator = Paginator(comments, 11)
        page = request.GET.get('page')
        comments = paginator.get_page(page)

        if request.method == "POST":
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment = request.POST.get('comment')
                Comments.objects.create(post=post, comments=comment, user=request.user)
        else:
            form = CommentsForm()

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "form": form,
        "comments": comments,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "post": post,
        'likes_count': post.likes_count(),
        "has_liked": has_liked,
        "comments_count": comments_count
    }

    if request.is_ajax():
        comment_string = render_to_string("users/group_post_comment_form.html", context, request=request)
        return JsonResponse({"form": comment_string})

    return render(request, "users/post_detail.html", context)


@login_required
def like_group_post(request, id):
    post = get_object_or_404(GroupPost, id=id)
    has_liked = False
    message = f"{request.user.username} liked your posts '{post.title}'"

    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
        has_liked = True

    else:
        post.likes.remove(request.user)
        has_liked = False

    context = {
        "post": post,
        "has_liked": has_liked,
        'likes_count': post.likes_count(),
    }

    if request.is_ajax():
        lpost = render_to_string("users/like_group_post.html", context, request=request)
        return JsonResponse({"depost": lpost})


@login_required
def all_groups_posts(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        group_posts = GroupPost.objects.all().order_by('-date_posted')
        my_notify = mynotifications(request.user)
        latest_groups = Group.objects.all().order_by('-date_created')[:10]

        paginator = Paginator(group_posts, 10)
        page = request.GET.get('page')
        group_posts = paginator.get_page(page)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "group_posts": group_posts,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "latest_groups": latest_groups,
    }

    return render(request, "users/group_post.html", context)

