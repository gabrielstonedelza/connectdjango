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
from .forms import (FeedbackForm, ContactUsForm, TutorialForm, CommentsForm, BlogPostForm, BlogUpdateForm, TutorialUpdateForm)
from .models import (Tutorial, Comments, FeedBack, ContactUs, BlogPost, NotifyMe)
from .notifications import mynotifications
from .process_mail import send_my_mail
from django.conf import settings



@login_required
def all_tutorial(request):
    my_notify = mynotifications(request.user)
    tutorials = Tutorial.objects.all().order_by('-date_posted')
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')[:5]

    paginator = Paginator(tutorials, 15)
    page = request.GET.get('page')
    tutorials = paginator.get_page(page)


    context = {
        "tutorials": tutorials,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "users": users
    }
    # send_my_mail("Hi",settings.EMAIL_HOST_USER,f"{request.user.email}",context,"email_templates/success.html")

    return render(request, "blog/tutorials.html", context)


@login_required
def create_tutorial(request):
    u_profile = get_object_or_404(Profile, user=request.user)
    user_followers = u_profile.followers.all()

    ufollowers_emails = []
    for i in user_followers:
        ufollowers_emails.append(i.email)

    my_notify = mynotifications(request.user)

    if request.method == "POST":
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            t_content = form.cleaned_data.get('tutorial_content')
            img = form.cleaned_data.get('image')

            Tutorial.objects.create(user=request.user, title=title, image=img, tutorial_content=t_content)
            # send_my_mail(f"New Tutorial from {request.user.username}", settings.EMAIL_HOST_USER,
            #             ufollowers_emails, f"{request.user.username} just posted a tutorial '{title}'")
            return redirect('tutorials')
    else:
        form = TutorialForm()

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/tutorial_form.html", context)


@login_required
def tutorial_detail(request, id):
    my_notify = mynotifications(request.user)
    tutorial = get_object_or_404(Tutorial, id=id)
    has_liked = False

    # message = f"{request.user.username} commented on your tutorial '{tutorial.title}'"
    if tutorial.likes.filter(id=request.user.id).exists():
        has_liked = True

    comments = Comments.objects.filter(tutorial=tutorial, reply=None).order_by('-date_posted')
    comments_count = comments.count()
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comments.objects.get(id=reply_id)
            comment = Comments.objects.create(tutorial=tutorial, user=request.user, comment=comment, reply=comment_qs)
            comment.save()
            # NotifyMe.objects.create(user=tutorial.user, notify_title="New Comment", notify_alert=message,
            #                             follower_sender=request.user,tuto_id=tutorial)

    else:
        form = CommentsForm()

    if tutorial:
        tutorial.views += 1
        tutorial.save()

    context = {
        "tutorial": tutorial,
        "has_liked": has_liked,
        "likes_count": tutorial.likes_count(),
        "comments": comments,
        "form": form,
        "comments_count": comments_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        comment = render_to_string("blog/comment_form.html", context, request=request)
        return JsonResponse({"comments": comment})

    return render(request, "blog/tutorial_detail.html", context)


@login_required
def like_tutorial(request, id):
    tutorial = get_object_or_404(Tutorial, id=id)
    has_liked = False

    if not tutorial.likes.filter(id=request.user.id).exists():
        tutorial.likes.add(request.user)
        has_liked = True

    else:
        tutorial.likes.remove(request.user)
        has_liked = False

    context = {
        "tutorial": tutorial,
        "has_liked": has_liked,
        "likes_count": tutorial.likes_count(),
    }
    if request.is_ajax():
        like = render_to_string("blog/like_form.html", context, request=request)
        return JsonResponse({"likes": like})


@login_required
def update_tutorial(request, id):
    tutorial = get_object_or_404(Tutorial, id=id)
    if request.method == "POST":
        form = TutorialUpdateForm(request.POST, instance=tutorial)
        if form.is_valid():
            form.save()
            messages.success(request, f"Tutorial was updated.")
            return redirect('tutorial_detail', tutorial.id)

    else:
        form = TutorialUpdateForm(instance=tutorial)

    context = {
        "form": form,
        "tutorial": tutorial
    }
    return render(request, "blog/tutorial_update.html", context)


class TutorialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tutorial
    success_url = '/tutorials'

    def test_func(self):
        tutorial = self.get_object()
        if self.request.user == tutorial.user:
            return True
        else:
            return False


@login_required
def blogs(request):
    my_notify = mynotifications(request.user)
    blog_posts = BlogPost.objects.all().order_by('-date_posted')
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')[:5]

    paginator = Paginator(blog_posts, 15)
    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)

    context = {
        "blog_posts": blog_posts,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "users": users
    }

    return render(request, "blog/blog_posts.html", context)


@login_required
def blog_detail(request, id):
    blog = get_object_or_404(BlogPost, id=id)
    my_notify = mynotifications(request.user)
    is_liked = False

    if blog.likes.filter(id=request.user.id).exists():
        is_liked = True

    if blog:
        blog.views += 1
        blog.save()

    context = {
        "blog": blog,
        "is_liked": is_liked,
        "likes_count": blog.likes_count(),
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/blog_detail.html", context)


@login_required
def like_blog(request, id):
    blog = get_object_or_404(BlogPost, id=id)
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
        like = render_to_string("blog/blog_like_form.html", context, request=request)
        return JsonResponse({"likes": like})


@login_required
def create_blog(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    user_followers = user_profile.followers.all()

    ufollowers_emails = []
    for i in user_followers:
        ufollowers_emails.append(i.email)
    my_notify = mynotifications(request.user)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            blog_img = form.cleaned_data.get('blog_image')

            BlogPost.objects.create(user=request.user, title=title, content=content, blog_image=blog_img)
            # send_my_mail(f"New Post from {request.user.username}", settings.EMAIL_HOST_USER,
            #             ufollowers_emails, f"{request.user.username} just posted a blog '{title}'")
            return redirect('all_blogs')
    else:
        form = BlogPostForm()

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/blog_post_form.html", context)


@login_required
def update_blog(request, id):
    blog = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        form = BlogUpdateForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blogpost_detail', blog.id)

    else:
        form = BlogUpdateForm(instance=blog)

    context = {
        "form": form,
        "blog": blog
    }
    return render(request, "blog/blog_update.html", context)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/all_blogs'

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.user:
            return True
        else:
            return False


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

    deUser = get_object_or_404(User, username=username)

    tutorials = Tutorial.objects.filter(user=deUser.id).order_by('-date_posted')
    blogs = BlogPost.objects.filter(user=deUser.id).order_by('-date_posted')

    paginator = Paginator(tutorials, 15)
    page = request.GET.get('page')
    tutorials = paginator.get_page(page)

    paginator = Paginator(blogs, 15)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    deuser_following = deUser.profile.following.all()
    deuser_followers = deUser.profile.followers.all()

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],

        "following": following,
        "followers": followers,
        "defollowing": deuser_following,
        "defollowers": deuser_followers,
        "deuser": deUser,
        "tutorials": tutorials,
        "blogs": blogs
    }

    return render(request, "blog/userpostprofile.html", context)


@login_required
def user_profile_following(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    deUser = get_object_or_404(User, username=username)
    defollowing = deUser.profile.following.all()
    defollowers = deUser.profile.followers.all()

    df_count = deUser.profile.following.all().count
    paginator = Paginator(defollowing, 10)
    page = request.GET.get('page')
    defollowing = paginator.get_page(page)

    context = {
        "following": following,
        "followers": followers,
        "defollowing": defollowing,
        "defollowers": defollowers,
        "deuser": deUser,
        "df_count": df_count
    }
    return render(request, "blog/deuserprofile_followings.html", context)


@login_required
def user_profile_followers(request, username):
    myprofile = get_object_or_404(Profile, user=request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()

    deUser = get_object_or_404(User, username=username)
    defollowing = deUser.profile.following.all()
    defollowers = deUser.profile.followers.all()

    dfs_count = deUser.profile.followers.all().count

    paginator = Paginator(defollowers, 10)
    page = request.GET.get('page')
    defollowers = paginator.get_page(page)

    context = {
        "following": following,
        "followers": followers,
        "defollowing": defollowing,
        "defollowers": defollowers,
        "deuser": deUser,
        "dfs_count": dfs_count
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
def feed_backs(request):
    all_feedbacks = FeedBack.objects.all().order_by('-date_posted')
    my_notify = mynotifications(request.user)
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
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        feedback = render_to_string("blog/my_feedbacks.html", context, request=request)
        return JsonResponse({"form": feedback})

    return render(request, "blog/feedback.html", context)


def contact_us(request):
    my_notify = mynotifications(request.user)
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            ContactUs.objects.create(name=name, email=email, subject=subject, message=message)

    else:
        form = ContactUsForm()

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        conform = render_to_string("blog/contact_form.html", context, request=request)
        return JsonResponse({"form": conform})

    return render(request, "blog/contact.html", context)


@login_required
def about_cd(request):
    return render(request, "blog/about_connectdjango.html")
