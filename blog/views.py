from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView
from django.template.loader import render_to_string
from .models import (Question, Answers, Tutorial, NotifyMe, FeedBack, ContactUs)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import (AnswerForm, TutorialForm, QuestionForm, FeedbackForm, ContactUsForm, TutorialUpdateForm)
from django.db.models import Q
from users.models import Profile, Group, GroupPost, LoginConfirmCode, LastSeen
from users.views import user_connection
from django.core.paginator import Paginator
from .notifications import mynotifications
from .process_mail import send_my_mail
from django.conf import settings
import sys
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


def login_request(request):
    uuser = ''
    has_login_code_already = False
    user_platform = sys.platform
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            uname = request.POST['username']
            upassword = request.POST['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)

                if not LoginConfirmCode.objects.filter(logged_user=user).exists():
                    LoginConfirmCode.objects.create(logged_user=user, logged_in_platform=user_platform)
                    return redirect('latest_questions')
                else:
                    messages.info(request,
                                  f"you already have an unexpired login token,meaning you have logged in on another device,please wait just a second and login again as we log you out of the other device")
                    euser = get_object_or_404(LoginConfirmCode, logged_user=user)
                    if euser:
                        euser.delete()
                    return redirect('login')
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
        "has_login_code_already": has_login_code_already
    }
    return render(request, "blog/home.html", context)


def latest_qs(request):
    latest_questions = []
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_logged_in_user = get_object_or_404(LoginConfirmCode, logged_user=request.user)
        users_dtime = my_logged_in_user.dtime
        my_notify = mynotifications(request.user)

        latest_questions = Question.objects.all().order_by('-date_posted').order_by('-date_posted')
        latest_groups = Group.objects.all().order_by('-date_created')[:5]

        paginator = Paginator(latest_questions, 10)
        page = request.GET.get('page')
        latest_questions = paginator.get_page(page)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "latest_questions": latest_questions,
        "users_dtime": users_dtime,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/latest_qs.html", context)


@login_required
def unanswered_qs(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        unanswered_questions = Question.objects.filter(answered=False).order_by("-date_posted")
        latest_groups = Group.objects.all().order_by('-date_created')[:5]
        my_notify = mynotifications(request.user)

        paginator = Paginator(unanswered_questions, 10)
        page = request.GET.get('page')
        unanswered_questions = paginator.get_page(page)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "unanswered_qs": unanswered_questions,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/unanswered_qs.html", context)


@login_required
def answered_questions(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        most_answered_qs = Question.objects.filter(answered=True).order_by("-date_posted")
        latest_groups = Group.objects.all().order_by('-date_created')[:5]
        my_notify = mynotifications(request.user)

        paginator = Paginator(most_answered_qs, 10)
        page = request.GET.get('page')
        most_answered_qs = paginator.get_page(page)
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "most_answered_qs": most_answered_qs,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/most_answered_qs.html", context)


@login_required
def latest_tutorials(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        recent_tutos = Tutorial.objects.filter(make_private=False).order_by("-date_posted")
        latest_groups = Group.objects.all().order_by('-date_created')[:5]
        my_notify = mynotifications(request.user)

        paginator = Paginator(recent_tutos, 10)
        page = request.GET.get('page')
        recent_tutos = paginator.get_page(page)
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "recent_tutos": recent_tutos,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/latest_tutorials.html", context)


@login_required
def most_viewed_tutorials(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        most_viewed_tutorials = Tutorial.objects.filter(views__gt=60).order_by("-date_posted")
        latest_groups = Group.objects.all().order_by('-date_created')[:5]
        my_notify = mynotifications(request.user)

        paginator = Paginator(most_viewed_tutorials, 10)
        page = request.GET.get('page')
        most_viewed_tutorials = paginator.get_page(page)
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "most_viewed_tutorials": most_viewed_tutorials,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/most_viewed_tuto.html", context)


@login_required
def locked_tutorials(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        private_tutorials = Tutorial.objects.filter(make_private=True)
        latest_groups = Group.objects.all().order_by('-date_created')[:5]
        my_notify = mynotifications(request.user)

        paginator = Paginator(private_tutorials, 10)
        page = request.GET.get('page')
        private_tutorials = paginator.get_page(page)
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "private_tutorials": private_tutorials,
        "latest_groups": latest_groups,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/locked_tutorials.html", context)


@login_required
def question_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        question = get_object_or_404(Question, id=id)
        answers = Answers.objects.filter(question=question, reply=None).order_by('-date_posted')
        my_notify = mynotifications(request.user)
        answers_count = answers.count()
        message = f"{request.user.username} answered your question '{question.question}'"

        paginator = Paginator(answers, 10)
        page = request.GET.get('page')
        answers = paginator.get_page(page)

        if Answers.objects.filter(question=question) and not Answers.objects.filter(answer=None):
            question.answered = True
            question.save()

        if question:
            question.views += 1
            question.save()

        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = request.POST.get('answer')
                reply_id = request.POST.get('answer_id')
                answer_qs = None
                if reply_id:
                    answer_qs = Answers.objects.get(id=reply_id)
                answer = Answers.objects.create(question=question, user=request.user, reply=answer_qs, answer=answer)
                answer.save()

                if not answer.user == question.question_author:
                    NotifyMe.objects.create(user=question.question_author, notify_title="Question Answered", notify_alert=message, follower_sender=request.user, que_id=question.id)

        else:
            form = AnswerForm()
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        'question': question,
        'form': form,
        'answers': answers,
        'answers_count': answers_count,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        html = render_to_string("blog/answer_form.html", context, request=request)
        return JsonResponse({'form': html})

    return render(request, "blog/question_detail.html", context)


@login_required
def tutorial_detail(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        tutorial = get_object_or_404(Tutorial, id=id)
        tutorials = Tutorial.objects.filter(make_private=False).order_by('-date_posted')[:10]
        my_notify = mynotifications(request.user)

        if tutorial:
            tutorial.views += 1
            tutorial.save()

        is_liked = False
        if tutorial.likes.filter(id=request.user.id).exists():
            is_liked = True

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        'tutorial': tutorial,
        'is_liked': is_liked,
        'likes_count': tutorial.likes_count(),
        'tutorials': tutorials,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    if request.is_ajax():
        html = render_to_string("blog/like_section.html",
                                context, request=request)
        return JsonResponse({
            "form": html
        })
    return render(request, "blog/tutorial_detail.html", context)


@login_required
def like_tutorial(request, id):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        tutorial = get_object_or_404(Tutorial, id=id)
        is_liked = False
        message = f"{request.user.username} liked your tutorial '{tutorial.title}'"

        if tutorial.likes.filter(id=request.user.id).exists():
            tutorial.likes.remove(request.user)
            is_liked = False
        else:
            tutorial.likes.add(request.user)
            is_liked = True

            NotifyMe.objects.create(user=tutorial.tutorial_author, notify_title="Liked Tutorial", notify_alert=message, follower_sender=request.user)
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "tutorial": tutorial,
        "is_liked": is_liked,
        "likes_count": tutorial.likes_count(),
    }
    if request.is_ajax():
        html = render_to_string("blog/like_section.html", context, request=request)
        return JsonResponse({
            "form": html
        })


@login_required
def create_question(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        user_profile = get_object_or_404(Profile, user=request.user)
        user_followers = user_profile.followers.all()
        message = f"New question from {request.user}"

        ufollowers_emails = []
        for i in user_followers:
            ufollowers_emails.append(i.email)

        my_notify = mynotifications(request.user)

        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.cleaned_data.get('question')
                q_description = form.cleaned_data.get('q_description')

                Question.objects.create(question_author=request.user, question=question, q_description=q_description)
                for i in user_followers:
                    NotifyMe.objects.create(user=i, notify_title="New Question", notify_alert=message, follower_sender=request.user)

                messages.success(request, f"Your question was posted successfully.")
                return redirect("latest_questions")

        else:
            form = QuestionForm()
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "form": form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }
    return render(request, "blog/question_form.html", context)


@login_required
def create_tutorial(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        user_profile = get_object_or_404(Profile, user=request.user)
        user_followers = user_profile.followers.all()
        message = f"New tutorial from {request.user}"

        ufollowers_emails = []
        for i in user_followers:
            ufollowers_emails.append(i.email)

        my_notify = mynotifications(request.user)

        is_made_private = False
        if request.method == "POST":
            form = TutorialForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                tutorial_content = form.cleaned_data.get('tutorial_content')
                if form.cleaned_data.get('make_private'):
                    is_made_private = True

                Tutorial.objects.create(tutorial_author=request.user, title=title, tutorial_content=tutorial_content,
                                        make_private=is_made_private)
                if not is_made_private:
                    for i in user_followers:
                        NotifyMe.objects.create(user=i, notify_title="New Tutorial", notify_alert=message, follower_sender=request.user)

                messages.success(request, f"Tutorial {title} added successfully.")
                return redirect('latest_tutorials')
        else:
            form = TutorialForm()

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        'form': form,
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
    }

    return render(request, "blog/tutorial_form.html", context)


@login_required
def update_tutorial(request, id):
    tutorial = get_object_or_404(Tutorial, id=id)
    if request.method == "POST":
        form = TutorialUpdateForm(request.POST, instance=tutorial)
        if form.is_valid():
            form.save()
            return redirect('tuto_detail', tutorial.id)

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
        if self.request.user == tutorial.tutorial_author:
            return True
        else:
            return False


@login_required
def all_tutorials(request):
    all_tutos = Tutorial.objects.all().order_by('-date_posted')
    u_notify1 = NotifyMe.objects.filter(user=request.user).order_by('-date_notified')
    u_notify = NotifyMe.objects.filter(user=request.user).filter(read=False).order_by('-date_notified')
    u_notify_count = u_notify.count()
    context = {
        'all_tutos': all_tutos,
        'notification': u_notify1,
        'unread_notification': u_notify,
        'u_notify_count': u_notify_count,
    }
    return render(request, "blog/all_tutos.html", context)


@login_required
def search_queries(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        query = request.GET.get('q', None)
        if query is not None:
            questions = Question.objects.filter(
                Q(question__icontains=query) |
                Q(question_author__username__icontains=query)
            )
            tutorials = Tutorial.objects.filter(
                Q(title__icontains=query) |
                Q(tutorial_author__username__icontains=query)
            )
            all_groups = Group.objects.filter(
                Q(group_name__icontains=query) |
                Q(group_leader__username__icontains=query)
            )
            all_group_posts = GroupPost.objects.filter(
                Q(title__icontains=query)
            )
    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        'questions': questions,
        'tutorials': tutorials,
        'all_groups': all_groups,
        'all_group_posts': all_group_posts,
    }
    if request.is_ajax():
        html = render_to_string("blog/search_list.html", context, request=request)
        return JsonResponse({
            'form': html
        })


@login_required
def user_post_profile(request, username):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)

        myprofile = get_object_or_404(Profile, user=request.user)

        following = myprofile.following.all()
        followers = myprofile.followers.all()

        deUser = get_object_or_404(User, username=username)
        deuser_following = deUser.profile.following.all()
        deuser_followers = deUser.profile.followers.all()

        upost_questions = Question.objects.filter(question_author=deUser).order_by('-date_posted')
        q_count = upost_questions.count()
        upost_tutorials = Tutorial.objects.filter(tutorial_author=deUser).order_by('-date_posted')
        t_count = upost_tutorials.count()

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "question_count": q_count,
        "tutorial_count": t_count,
        "upost_tutorials": upost_tutorials,
        "upost_questions": upost_questions,
        "following": following,
        "followers": followers,
        "defollowing": deuser_following,
        "defollowers": deuser_followers,
        "deuser": deUser,
    }

    return render(request, "blog/userpostprofile.html", context)


@login_required
def explore_new(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)

        myprofile = get_object_or_404(Profile, user=request.user)
        following = myprofile.following.all()
        new_users = User.objects.exclude(id=request.user.id).order_by('-date_joined')[:15]
        groups = Group.objects.all().order_by('-date_created')[:15]
        user = request.user

        not_following = []
        for i in new_users:
            if i not in following:
                not_following.append(i)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "new_users": new_users,
        "not_following": not_following,
        "groups": groups,
        "user": user,
    }

    if request.is_ajax():
        gg = render_to_string("blog/join_or_exit_group.html", context, request=request)
        return JsonResponse({"form": gg})

    return render(request, "blog/explore_new.html", context)


@login_required
def new_to_dja(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)

        myprofile = get_object_or_404(Profile, user=request.user)
        following = myprofile.following.all()
        new_users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
        groups = Group.objects.all().order_by('-date_created')

        not_following = []
        for i in new_users:
            if i not in following:
                not_following.append(i)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('home')

    context = {
        "notification": my_notify['notification'],
        "unread_notification": my_notify['unread_notification'],
        "u_notify_count": my_notify['u_notify_count'],
        "has_new_notification": my_notify['has_new_notification'],
        "new_users": new_users,
        "not_following": not_following,
        "groups": groups,
    }
    return render(request, "blog/new_to_djangoacross.html", context)


@login_required
def user_notifications(request):
    if LoginConfirmCode.objects.filter(logged_user=request.user).exists():
        my_notify = mynotifications(request.user)

        if request:
            for i in my_notify['notification']:
                if not i.read:
                    i.read = True
                    i.save()

        paginator = Paginator(my_notify['notification'], 10)
        page = request.GET.get('page')
        my_notify['notification'] = paginator.get_page(page)

    else:
        messages.info(request, f"Sorry we cannot find your login details")
        return redirect('login')

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


def contact_us(request):
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
        "form": form
    }

    if request.is_ajax():
        conform = render_to_string("blog/contact_form.html", context, request=request)
        return JsonResponse({"form": conform})

    return render(request, "blog/contact.html", context)


@login_required
def about_cd(request):
    return render(request, "blog/about_connectdjango.html")
