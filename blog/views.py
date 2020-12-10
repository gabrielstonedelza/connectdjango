from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from users.models import Profile
from .forms import (FeedbackForm, BlogForm, CommentsForm, BlogUpdateForm, ChatRoomCreateForm, ChatRoomUpdateForm, )
from .models import (FeedBack, NotifyMe, ChatRoom, Message, PrivateMessage, Blog, Comments, Chatters)
from .notifications import mynotifications
from .process_mail import send_my_mail
from django.conf import settings
from django.utils.safestring import mark_safe
import json
import random
from django.contrib import messages


def csrf_failure(request, reason=""):
    return render(request, "blog/403_csrf.html")


def chat_rooms(request):
    all_rooms = ChatRoom.objects.all().order_by('-date_created')
    my_notify = mynotifications(request.user)
    your_room_count = 5
    can_create_room = False

    my_rooms = ChatRoom.objects.filter(creator=request.user)

    if my_rooms.count() < your_room_count:
        can_create_room = True
    else:
        can_create_room = False
  

    context = {
        "chatrooms": all_rooms,
        "my_rooms": my_rooms,
        "can_create_room": can_create_room,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/chatrooms.html", context)


@login_required
def private_chat(request, chat_id):
    my_notify = mynotifications(request.user)
    # chatid = get_object_or_404(PrivateMessage, chat_id=chat_id)
    chatid = get_object_or_404(Chatters, private_chat_id=chat_id)

    context = {
        'chat_id': mark_safe(json.dumps(chatid.id)),
        'username': mark_safe(json.dumps(request.user.username)),
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, 'blog/private_chat.html', context)


@login_required
def messages(request):
    my_notify = mynotifications(request.user)
    all_chats = Chatters.objects.all()
    chatters_id = ''
    chat_before = False
    my_new_chat_users = []
    my_chatters = []
    users = {}

    for i in all_chats:
        if request.user.username in i.chatter_users:
            if PrivateMessage.objects.filter(chat_id=i.chatter_users).exists():
                chat_before = True
                users[i.chatter_users.replace(request.user.username, '')] = i.private_chat_id
                if not i.chatter_users.replace(request.user.username, '') in my_chatters:
                    my_chatters.append(i.chatter_users.replace(request.user.username, ''))
                print(my_chatters)
    print(all_chats)
    context = {
        "all_chats": all_chats,
        "users": users,
        "my_new_chat_users": my_new_chat_users,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        # "chatters_id": chatters_id,
        "my_chatters": my_chatters,
    }
    return render(request, "blog/my_messages_inbox.html", context)


@login_required
def room_detail(request, slug):
    all_rooms = ChatRoom.objects.all().order_by('-date_created')
    room = get_object_or_404(ChatRoom, slug=slug)
    my_notify = mynotifications(request.user)
    is_creator = False
    print(request.session)

    my_room_members = room.allowed_users.all()
    pending_list = room.pending_users.all()
    pending_count = pending_list.count
    users = User.objects.exclude(id=request.user.id)
    if room.creator == request.user:
        is_creator = True

    context = {
        'room_name': mark_safe(json.dumps(room.id)),
        'username': mark_safe(json.dumps(request.user.username)),
        "room": room,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "my_room_members": my_room_members,
        "users": users,
        "is_creator": is_creator,
        "pending_list": pending_list,
        "pending_count": pending_count,
        "chatrooms": all_rooms,
    }
    return render(request, 'blog/room.html', context)


@login_required
def create_chatroom(request):
    my_notify = mynotifications(request.user)
    is_active = False
    allow_any = False
    success_message = ''
    error_message = ''

    if request.method == "POST":
        form = ChatRoomCreateForm(request.POST, request.FILES)
        if form.is_valid():
            room_name = form.cleaned_data.get('room_name')

            about = form.cleaned_data.get('about')
            room_logo = form.cleaned_data.get('room_logo')
            if form.cleaned_data.get('is_active'):
                is_active = True
            ChatRoom.objects.create(room_name=room_name, creator=request.user, about=about, room_logo=room_logo, is_active=is_active)
            success_message = 'room created'
            return redirect('chatrooms')
        else:
            error_message = "sorry something went wrong"

    else:
        form = ChatRoomCreateForm()

    context = {
        "form": form,
        "success_message": success_message,
        "error_message": error_message,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/chatroom_create_form.html", context)


@login_required
def update_room(request, slug):
    room = get_object_or_404(ChatRoom, slug=slug)
    my_notify = mynotifications(request.user)
    success_msg = ''

    if request.method == "POST":
        form = ChatRoomUpdateForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            success_msg = "your room was updated"
    else:
        form = ChatRoomUpdateForm(instance=room)

    context = {
        "form": form,
        "room": room,
        "success_msg": success_msg,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/chatroom_update_form.html", context)


@login_required
def add_to_room(request, id):
    room = get_object_or_404(ChatRoom, creator=request.user)
    user = get_object_or_404(User, id=id)
    my_room_members = room.allowed_users.all()
    pending_list = room.pending_users.all()
    users = User.objects.exclude(id=request.user.id)
    is_creator = False
    is_member = False
    if user in my_room_members:
        is_member = True
    else:
        is_member = False

    if not room.allowed_users.filter(id=user.id).exists():
        room.allowed_users.add(user)
        notify_message = f"Hi {user.username}, {room.creator} added you to {room.room_name}."
        NotifyMe.objects.create(user=user, notify_title=f"Added to room", notify_alert=notify_message,
                                follower_sender=request.user, room_slug=room.slug)

    if room.creator == request.user:
        is_creator = True

    context = {
        "room": room,
        "my_room_members": my_room_members,
        "users": users,
        "is_creator": is_creator,
        "is_member": is_member,
        "pending_list": pending_list,
    }

    if request.is_ajax():
        can_communicate = render_to_string("blog/add_members.html", context, request=request)
        return JsonResponse({
            "can_chat": can_communicate
        })


@login_required
def add_pending_members(request, id):
    room = get_object_or_404(ChatRoom, creator=request.user)
    user = get_object_or_404(User, id=id)
    my_room_members = room.allowed_users.all()
    pending_list = room.pending_users.all()
    users = User.objects.exclude(id=request.user.id)

    if not room.allowed_users.filter(id=user.id).exists():
        room.allowed_users.add(user)
        room.pending_users.remove(user)
        notify_message = f"Hi {user.username}, {room.creator} accepted your request and added you to {room.room_name}."
        NotifyMe.objects.create(user=user, notify_title=f"Request Accepted", notify_alert=notify_message,
                                follower_sender=request.user, room_slug=room.slug)

    context = {
        "room": room,
        "my_room_members": my_room_members,
        "users": users,
        "pending_list": pending_list,
    }

    if request.is_ajax():
        add_pending_member = render_to_string("blog/add_pending_members.html", context, request=request)
        return JsonResponse({
            "pending": add_pending_member
        })


@login_required
def join_room(request, slug):
    room = get_object_or_404(ChatRoom, slug=slug)
    room_members = room.allowed_users.all()
    pending_list = room.pending_users.all()
    success_message = ''

    if not room.allowed_users.filter(id=request.user.id).exists() and not room.pending_users.filter(
            id=request.user.id).exists():
        room.pending_users.add(request.user)
        notify_message = f"hi {room.creator}, {request.user.username} wants to join your room"
        NotifyMe.objects.create(user=room.creator, notify_title=f"Wants to join", notify_alert=notify_message,
                                follower_sender=request.user, room_slug=room.slug)

    context = {
        'room': room,
        'room_members': room_members,
        'pending_list': pending_list,
    }

    if request.is_ajax():
        room = render_to_string("blog/join_room.html", context, request=request)
        return JsonResponse({
            "joinroom": room
        })


@login_required
def need_access(request, slug):
    my_notify = mynotifications(request.user)
    form = ''

    room = get_object_or_404(ChatRoom, slug=slug)
    room_members = room.allowed_users.all()
    pending_list = room.pending_users.all()

    context = {
        "room": room,
        "room_members": room_members,
        "pending_list": pending_list,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/need_access.html", context)


@login_required
def blogs(request):
    all_blogs = Blog.objects.all().order_by('-date_posted')
    my_notify = mynotifications(request.user)
    context = {
        "blogs": all_blogs,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],

    }

    return render(request, "blog/blogs.html", context)


@login_required
def create_blog(request):
    my_notify = mynotifications(request.user)
    success_message = ""
    error_message = ""

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            subtitle = form.cleaned_data.get('subtitle')
            blogimg = form.cleaned_data.get('blog_pic')
            blogcontent = form.cleaned_data.get('blog_content')
            Blog.objects.create(user=request.user, title=title, subtitle=subtitle, blog_pic=blogimg,
                                blog_content=blogcontent)
            return redirect('blogs')

        else:
            error_message = "sorry something went wrong"
    else:
        form = BlogForm()

    context = {
        "form": form,
        "error_message": error_message,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/blog_create_form.html", context)


@login_required
def blog_detail(request, slug):
    my_notify = mynotifications(request.user)
    blog = get_object_or_404(Blog, slug=slug)
    is_liked = False

    comments = Comments.objects.filter(blog=blog).order_by('-date_posted')
    comments_count = comments.count()

    form = CommentsForm()
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
            comment = Comments.objects.create(user=request.user, blog=blog, comment=comment)
            comment.save()

        else:
            form = CommentsForm()

    if blog.likes.filter(id=request.user.id).exists():
        is_liked = True

    if blog:
        blog.views += 1
        blog.save()

    context = {
        "form": form,
        "blog": blog,
        "comments": comments,
        "is_liked": is_liked,
        "likes_count": blog.likes_count(),
        "comments_count": comments_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        comment = render_to_string("blog/comment_form.html", context, request=request)
        return JsonResponse({"comments": comment})

    return render(request, "blog/blog_detail.html", context)


@login_required
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    my_notify = mynotifications(request.user)
    success = ''

    if request.method == "POST":
        form = BlogUpdateForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            success = "Blog updated"
            return redirect('blog_detail', blog.slug)
    else:
        form = BlogUpdateForm(instance=blog)

    context = {
        "blog": blog,
        "form": form,
        "success": success,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/blog_update.html", context)


def like_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    is_liked = False

    if not blog.likes.filter(id=request.user.id).exists():
        blog.likes.add(request.user)
        is_liked = True
    else:
        blog.likes.remove(request.user)
        is_liked = False

    context = {
        "blog": blog,
        "is_liked": is_liked,
        "likes_count": blog.likes_count()
    }

    if request.is_ajax():
        likeblog = render_to_string("blog/like_section.html", context, request=request)
        return JsonResponse({"like": likeblog})


def news_letter(request):
    all_users = User.objects.exclude(id=request.user.id)

    for i in all_users:
        if i.email:
            send_my_mail(f"Hi from ConnectDjango", settings.EMAIL_HOST_USER, i.email, {"name": i.username},
                         "email_templates/success.html")
    messages.success(request, "Newsletter sent")

    return render(request, "blog/newsletter.html")


@login_required
def search_queries(request):
    global search_blogs, rooms
    query = request.GET.get('q', None)
    if query is not None:
        search_blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(subtitle__icontains=query)
        )
        rooms = ChatRoom.objects.filter(
            Q(room_name__icontains=query) |
            Q(creator__username__icontains=query)
        )

    context = {
        'blogs': search_blogs,
        'rooms': rooms,
    }
    if request.is_ajax():
        html = render_to_string("blog/search_list.html", context, request=request)
        return JsonResponse({
            'form': html
        })


@login_required
def user_profile(request, username):
    my_notify = mynotifications(request.user)
    are_chatters = False
    all_chatters = Chatters.objects.all()
    chatters_id = ''

    myprofile = get_object_or_404(Profile, user=request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    # user's username
    deuser = get_object_or_404(User, username=username)
    c_id = random.randint(1, 999999999)

    u_name1 = request.user.username
    u_name2 = deuser.username
    chat_names1 = f"{u_name1}{u_name2}"

    if not deuser.profile.chat_with.filter(id=request.user.id).exists() and not request.user.profile.chat_with.filter(
            id=deuser.id).exists():
        deuser.profile.chat_with.add(request.user)
        request.user.profile.chat_with.add(deuser)
        Chatters.objects.create(chatter_users=chat_names1, private_chat_id=f"{chat_names1}", sender=request.user,
                                receiver=deuser)

    for i in all_chatters.all():
        if request.user.username + deuser.username == i.chatter_users or deuser.username + request.user.username == i.chatter_users:
            are_chatters = True
            chatters_id = i.private_chat_id

    df_count = deuser.profile.following.all().count
    dfs_count = deuser.profile.followers.all().count

    user_blogs = Blog.objects.filter(user=deuser.id).order_by('-date_posted')
    blog_count = user_blogs.count()

    paginator = Paginator(user_blogs, 15)
    page = request.GET.get('page')
    user_blogs = paginator.get_page(page)

    deuser_following = deuser.profile.following.all()
    deuser_followers = deuser.profile.followers.all()

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "following": following,
        "followers": followers,
        "defollowing": deuser_following,
        "defollowers": deuser_followers,
        "deuser": deuser,
        "blogs": user_blogs,
        "df_count": df_count,
        "dfs_count": dfs_count,
        'blog_count': blog_count,
        "all_chatters": all_chatters,
        'chatters_id': chatters_id,
    }

    return render(request, "blog/userpostprofile.html", context)


@login_required
def user_profile_following(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)
    my_notify = mynotifications(request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    deUser = get_object_or_404(User, username=username)
    defollowing = deUser.profile.following.all()
    defollowers = deUser.profile.followers.all()

    df_count = deUser.profile.following.all().count
    dfs_count = deUser.profile.followers.all().count

    paginator = Paginator(defollowing, 10)
    page = request.GET.get('page')
    defollowing = paginator.get_page(page)

    context = {
        "following": following,
        "followers": followers,
        "defollowing": defollowing,
        "defollowers": defollowers,
        "deuser": deUser,
        "df_count": df_count,
        "dfs_count": dfs_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/deuserprofile_followings.html", context)


@login_required
def user_profile_followers(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)
    my_notify = mynotifications(request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    deUser = get_object_or_404(User, username=username)
    defollowing = deUser.profile.following.all()
    defollowers = deUser.profile.followers.all()

    dfs_count = deUser.profile.followers.all().count
    df_count = deUser.profile.following.all().count

    paginator = Paginator(defollowers, 10)
    page = request.GET.get('page')
    defollowers = paginator.get_page(page)

    context = {
        "following": following,
        "followers": followers,
        "defollowing": defollowing,
        "defollowers": defollowers,
        "deuser": deUser,
        "dfs_count": dfs_count,
        "df_count": df_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/deuserprofile_followers.html", context)


@login_required
def user_notifications(request):
    my_notify = mynotifications(request.user)

    if request:
        for i in my_notify['notification']:
            if not i.read:
                i.read = True
                i.save()

    paginator = Paginator(my_notify['notification'], 10)
    page = request.GET.get('page')
    my_notify['notification'] = paginator.get_page(page)

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/notifications.html", context)


@login_required
def about_cd(request):
    return render(request, "blog/about_connectdjango.html")


@login_required
def feed_backs(request):
    all_feedbacks = FeedBack.objects.all().order_by('-date_posted')

    paginator = Paginator(all_feedbacks, 10)
    page = request.GET.get('page')
    all_feedbacks = paginator.get_page(page)

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data.get('feedback')
            FeedBack.objects.create(user=request.user, feedback=feedback)
    else:
        form = FeedbackForm()

    context = {
        "all_feedbacks": all_feedbacks,
        "form": form
    }

    if request.is_ajax():
        feedback = render_to_string("blog/my_feedbacks.html", context, request=request)
        return JsonResponse({"form": feedback})

    return render(request, "blog/feedback.html", context)
