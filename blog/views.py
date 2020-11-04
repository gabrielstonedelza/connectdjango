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
from .forms import (FeedbackForm, ContactUsForm, TutorialForm, CommentsForm, BlogPostForm, BlogUpdateForm,
                    TutorialUpdateForm, ImproveTutoForm, ImproveTutoCommentsForm)
from .models import (Tutorial, Comments, FeedBack, ContactUs, BlogPost, NotifyMe, ImproveTuto, ImproveTutoComments)
from .notifications import mynotifications
from .process_mail import send_my_mail
from django.conf import settings
import imghdr


def csrf_failure(request, reason=""):

    return render(request,"blog/403_csrf.html")
    


@login_required
def news_letter(request):
    all_users = User.objects.exclude(id=request.user.id)
   

    for i in all_users:
        if i.email:
            send_my_mail(f"Hi from ConnectDjango", settings.EMAIL_HOST_USER, i.email, {"name":i.username}, "email_templates/success.html")
    messages.success(request,"Newsletter sent")

    return render(request, "blog/newsletter.html")


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
        "users": users,
        "name": request.user.username,

    }
    

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
            for ff in user_followers:
                send_my_mail(f"New tutorial from {request.user.username}", settings.EMAIL_HOST_USER, ff.email, {"name":ff.username,"title": title,"creator": request.user.username}, "email_templates/tutorial_create_success.html")
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
def tutorial_improvements(request,id):
    # tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    improvement = get_object_or_404(ImproveTuto, id=id)
    comments = ImproveTutoComments.objects.filter(improvetutocomment=improvement).order_by('-date_posted')
    my_notify = mynotifications(request.user)

    if improvement:
        improvement.views +=1
        improvement.save()
    # comment form 
    if request.method == 'POST':
        form = ImproveTutoCommentsForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
           
            comment = ImproveTutoComments.objects.create(improvetutocomment=improvement, user=request.user, comment=comment)
            comment.save()

    else:
        form = ImproveTutoCommentsForm()

    context = {
        # "tutorial": tutorial,
        "improvement": improvement,
        "form": form,
        "comments": comments,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        comment = render_to_string("blog/improvement_comment_form.html", context, request=request)
        return JsonResponse({"comments": comment})

    return render(request, "blog/improvement_detail.html", context)
    

@login_required
def tutorial_detail(request, id):
    my_notify = mynotifications(request.user)
    tutorial = get_object_or_404(Tutorial, id=id)
    has_liked = False

    if tutorial.likes.filter(id=request.user.id).exists():
        has_liked = True

    comments = Comments.objects.filter(tutorial=tutorial).order_by('-date_posted')
    comments_count = comments.count()

    improvements = ImproveTuto.objects.filter(tuto=tutorial).order_by('-date_posted')

    # comment form 
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
           
            comment = Comments.objects.create(tutorial=tutorial, user=request.user, comment=comment)
            comment.save()

    else:
        form = CommentsForm()

    # improvement form
    if request.method == "POST":
        improvement_form = ImproveTutoForm(request.POST)
        if improvement_form.is_valid():
            title = improvement_form.cleaned_data.get('title')
            can_be_modified = improvement_form.cleaned_data.get('can_be_modified')
            improvement_or_change = improvement_form.cleaned_data.get('improvement_or_change')
            ImproveTuto.objects.create(tuto=tutorial, user=request.user,title=title, can_be_modified=can_be_modified, improvement_or_change=improvement_or_change)
            messages.success(request, f"Notification is sent to {tutorial.user.username} about this suggested improvement,thank you {request.user.username}.")
            return redirect('tutorial_detail', tutorial.id)

    else:
        improvement_form = ImproveTutoForm()

    if tutorial:
        tutorial.views += 1
        tutorial.save()

    context = {
        "tutorial": tutorial,
        "has_liked": has_liked,
        "likes_count": tutorial.likes_count(),
        "comments": comments,
        "form": form,
        "improvement_form": improvement_form,
        "comments_count": comments_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "improvements": improvements
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
        form = TutorialUpdateForm(request.POST,request.FILES, instance=tutorial)
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
            for ff in user_followers:
                send_my_mail(f"New blog from {request.user.username}", settings.EMAIL_HOST_USER, ff.email, {"name":ff.username,"title": title,"creator": request.user.username}, "email_templates/blog_create_success.html")
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
        form = BlogUpdateForm(request.POST, request.FILES, instance=blog)
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
def user_profile(request,username):
    my_notify = mynotifications(request.user)

    myprofile = get_object_or_404(Profile, user=request.user)

    following = myprofile.following.all()
    followers = myprofile.followers.all()


    # user's username
    deuser = get_object_or_404(User, username=username)
    df_count = deuser.profile.following.all().count
    dfs_count = deuser.profile.followers.all().count

    tutorials = Tutorial.objects.filter(user=deuser.id).order_by('-date_posted')
    blogs = BlogPost.objects.filter(user=deuser.id).order_by('-date_posted')

    paginator = Paginator(tutorials, 15)
    page = request.GET.get('page')
    tutorials = paginator.get_page(page)

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
        "tutorials": tutorials,
        "blogs": blogs,
        "df_count": df_count,
        "dfs_count": dfs_count,
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


