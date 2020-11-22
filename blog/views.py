from django.contrib import messages
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
from .forms import (FeedbackForm,BlogForm, CommentsForm,BlogUpdateForm)
from .models import (FeedBack, NotifyMe, ChatRoom,Message,PrivateMessage, Blog, Comments,LoginConfirmCode)
from .notifications import mynotifications
from .process_mail import send_my_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login



def login_request(request):
    randcode = random.randint(1, 100000000)

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            uname = request.POST['username']
            upassword = request.POST['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)
                if not LoginConfirmCode.objects.filter(logged_user=user).exists():
                    LoginConfirmCode.objects.create(logged_user=user, user_login_code=randcode)
                else:
                    return redirect('django_time')
                return redirect('django_time')
    else:
        form = AuthenticationForm()
    context = {
        "form": form
    }
    return render(request, "users/login.html", context)


def logout_request(request):
    try:
        ul = DjangoTime.objects.filter(user=request.user)
        ul1 = LoginConfirmCode.objects.filter(logged_user=request.user)
        if ul:
            ul.delete()
            ul1.delete()

    except LookupError as e:
        messages.info(request, f"User details relating to your information does not exist,{e}")

    return render(request, "users/logout.html")

def csrf_failure(request, reason=""):
    return render(request, "blog/403_csrf.html")

def chatrooms(request):
    chatrooms = ChatRoom.objects.all().order_by('-date_created')

    context = {
        "chatrooms": chatrooms
    }

    return render(request,"blog/chatrooms.html",context)

@login_required
def room_detail(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    online_users = UsersCheckedIn.objects.filter(check_date=datetime.today()).order_by('-check_date')
    users = []
    for i in online_users.all():
        users.append(i.user)
        if request.user in users:
            users.remove(request.user)

    context = {
        'room_name': mark_safe(json.dumps(room.id)),
        'username': mark_safe(json.dumps(request.user.username)),
        "user_has_checked_in": mycheck['user_has_checked_in'],
        "online_users": online_users,
        "users": users,
        "room": room
    }
    return render(request, 'blog/room.html', context)

@login_required
def blogs(request):
    blogs = Blog.objects.all().order_by('-date_posted')
    context = {
        "blogs": blogs
    }

    return render(request,"blog/blogs.html",context)


@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            subtitle = form.cleaned_data.get('subtitle')
            blogimg = form.cleaned_data.get('blog_pic')
            blogcontent = form.cleaned_data.get('blog_content')
            Blog.objects.create(user=request.user,title=title,subtitle=subtitle,blog_pic=blogimg,blog_content=blogcontent)
            messages.success(request,f"Successfully created {title}")
            return redirect('blogs')

        else:
            messages.info(request,"sorry something went wrong")
    else:
        form = BlogForm()

    context = {
        "form": form
    }

    return render(request,"blog/blog_create_form.html",context)


@login_required
def blog_detail(request,title):
    blog = get_object_or_404(Blog,title=title)
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
    }

    if request.is_ajax():
        comment = render_to_string("blog/comment_form.html",context,request=request)
        return JsonResponse({"comments": comment})

    return render(request,"blog/blog_detail.html",context)

@login_required
def blog_update(request,title):
    blog = get_object_or_404(Blog, title=title)

    if request.method == "POST":
        form = BlogUpdateForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request,"Blog updated")
            return redirect('blog_detail',blog.title)
    else:
        form = BlogUpdateForm(instance=blog)

    context = {
        "blog": blog,
        "form": form
    }

    return render(request,"blog/blog_update.html",context)


def like_blog(request,title):
    blog = get_object_or_404(Blog,title=title)
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
        likeblog = render_to_string("blog/like_section.html", context,request=request)
        return JsonResponse({ "like": likeblog })


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
    query = request.GET.get('q', None)
    if query is not None:
        tutorials = Tutorial.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query)
        )
        search_blogs = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query)
        )

    context = {
        'blogs': search_blogs,
        'tutorials': tutorials,
    }
    if request.is_ajax():
        html = render_to_string("blog/search_list.html", context, request=request)
        return JsonResponse({
            'form': html
        })


@login_required
def user_profile(request, username):
    my_notify = mynotifications(request.user)

    myprofile = get_object_or_404(Profile, user=request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    # user's username
    deuser = get_object_or_404(User, username=username)
    df_count = deuser.profile.following.all().count
    dfs_count = deuser.profile.followers.all().count

    blogs = Blog.objects.filter(user=deuser.id).order_by('-date_posted')
    blog_count = blogs.count()

    paginator = Paginator(blogs, 15)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

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
        "blogs": blogs,
        "df_count": df_count,
        "dfs_count": dfs_count,
        'blog_count': blog_count
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
