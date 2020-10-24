from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView

from users.models import Profile
from .forms import (FeedbackForm, ContactUsForm, ProjectFilesForm, Project_Issue_Form, FixForm, ProjectFilesUpdateForm)
from .models import (Project, ProjectFiles, ProjectIssues, Issues, FixProjectIssue, FeedBack, ContactUs)
from .notifications import mynotifications


@login_required
def all_projects(request):
    projects = Project.objects.all().order_by('-date_created')
    total_projects = projects.count()
    all_issues_count = Issues.objects.all()
    project_issues = ProjectIssues.objects.all()
    issues = all_issues_count.count() + project_issues.count()
    users = User.objects.all()

    paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    projects = paginator.get_page(page)

    context = {
        "projects": projects,
        "tprojects": total_projects,
        "all_issues": issues,
        "users": users
    }

    return render(request, "blog/projects.html", context)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_title', 'contributors', 'project_description', 'short_description_for_project', 'project_logo']
    success_url = "/projects"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def project_detail(request, project_name):
    project = get_object_or_404(Project, project_title=project_name)
    pp = Project.objects.filter(project_title=project)
    project_files = ProjectFiles.objects.filter(project=project)
    project_issues = ProjectIssues.objects.filter(project_with_issue=project)

    paginator = Paginator(project_files, 10)
    page = request.GET.get('page')
    project_files = paginator.get_page(page)

    if project:
        project.views += 1
        project.save()

    # add a new project file
    if request.method == "POST":
        form = ProjectFilesForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('file_name')
            code = form.cleaned_data.get('code')
            ProjectFiles.objects.create(project=project, user=request.user, file_name=fname, code=code)
            messages.success(request, f"File added successfully.")
            return redirect('files_in', project.id)
    else:

        form = ProjectFilesForm()

    context = {
        "project": project,
        "project_files": project_files,
        "p_issues": project_issues,
        "form": form,
        "pp": pp
    }

    return render(request, "blog/project_detail.html", context)


@login_required
def project_file_detail(request, id):
    project_file = get_object_or_404(ProjectFiles, id=id)
    has_approved = False

    if project_file.approves.filter(id=request.user.id).exists():
        has_approved = True

    context = {
        "project_file": project_file,
        "has_approved": has_approved
    }

    return render(request, "blog/project_file_detail.html", context)


@login_required
def project_file_update(request, id):
    project_file = get_object_or_404(ProjectFiles, id=id)

    if request.method == "POST":
        form = ProjectFilesUpdateForm(request.POST, instance=project_file)
        if form.is_valid():
            form.save()
            messages.success(request, f"File was updated")
    else:
        form = ProjectFilesUpdateForm(instance=project_file)

    context = {
        "project_file": project_file,
        "form": form
    }

    return render(request, "blog/projectfiles_form.html", context)


@login_required
def issues_fixes(request, project_name):
    issued_project = get_object_or_404(Project, project_title=project_name)
    project_with_issues = ProjectIssues.objects.filter(project_with_issue=issued_project).order_by('-date_posted')
    project_with_issues_count = project_with_issues.count()

    paginator = Paginator(project_with_issues, 10)
    page = request.GET.get('page')
    project_with_issues = paginator.get_page(page)

    # addressing an issue
    if request.method == "POST":
        issue_form = Project_Issue_Form(request.POST)
        if issue_form.is_valid():
            issue = issue_form.cleaned_data.get('issue')
            ProjectIssues.objects.create(project_with_issue=issued_project, user=request.user, issue=issue)
            # messages.success(request, f"Thanks {request.user.username},your issued would be reviewed")
    else:
        issue_form = Project_Issue_Form()

    context = {
        "issued_project": issued_project,
        "project_with_issues": project_with_issues,
        "issue_form": issue_form,
        "project_with_issues_count": project_with_issues_count,
    }

    if request.is_ajax():
        is_issuing = render_to_string("blog/issuing_form.html", context, request=request)
        return JsonResponse({"issuing": is_issuing})

    return render(request, "blog/issues&fixes.html", context)


@login_required
def project_issue_detail(request, id):
    project = get_object_or_404(ProjectIssues, id=id)
    all_fixes = FixProjectIssue.objects.filter(issue=project).order_by('-date_posted')
    fixes_count = all_fixes.count()

    if request.method == "POST":
        form = FixForm(request.POST)
        if form.is_valid():
            fix = form.cleaned_data.get('fix')
            my_fix = FixProjectIssue.objects.create(issue=project, user=request.user, fix=fix)
            my_fix.save()
    else:
        form = FixForm()

    context = {
        "form": form,
        "project": project,
        "all_fixes": all_fixes,
        "fixes_count": fixes_count
    }
    if request.is_ajax():
        pissue = render_to_string("blog/fix_form.html", context, request=request)
        return JsonResponse({"issue": pissue})

    return render(request, "blog/project_issue_detail.html", context)


@login_required
def files_in(request, id):
    project = get_object_or_404(Project, id=id)
    all_files = ProjectFiles.objects.filter(project=project).order_by('-date_posted')

    paginator = Paginator(all_files, 10)
    page = request.GET.get('page')
    all_files = paginator.get_page(page)

    context = {
        "all_files": all_files,
        "project": project
    }
    return render(request, "blog/file_in_stock.html", context)


@login_required
def approve_code(request, id):
    project_file = get_object_or_404(ProjectFiles, id=id)

    has_approved = False
    if not project_file.approves.filter(id=request.user.id).exists():
        project_file.approves.add(request.user)
        has_approved = True

    context = {
        "project_file": project_file,
        "has_approved": has_approved
    }

    if request.is_ajax():
        pfile = render_to_string("blog/approve_file.html", context, request=request)
        return JsonResponse({"file": pfile})


@login_required
def search_queries(request):
    query = request.GET.get('q', None)
    # if query is not None:
    #     questions = Question.objects.filter(
    #         Q(question__icontains=query) |
    #         Q(question_author__username__icontains=query)
    #     )
    #     tutorials = Tutorial.objects.filter(
    #         Q(title__icontains=query) |
    #         Q(tutorial_author__username__icontains=query)
    #     )
    #     all_groups = Group.objects.filter(
    #         Q(group_name__icontains=query) |
    #         Q(group_leader__username__icontains=query)
    #     )
    #     all_group_posts = GroupPost.objects.filter(
    #         Q(title__icontains=query)
    #     )

    context = {
        # 'questions': questions,
        # 'tutorials': tutorials,
        # 'all_groups': all_groups,
        # 'all_group_posts': all_group_posts,
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
    }

    return render(request, "blog/userpostprofile.html", context)


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
