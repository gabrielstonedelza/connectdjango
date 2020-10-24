import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=150, help_text="Title of your project", unique=True)
    contributors = models.ManyToManyField(User, related_name="wants_to_contribute",
                                          help_text="Invite other users to help build this project with you.Hold Ctrl "
                                                    "and click to add")
    likes = models.ManyToManyField(User, related_name="project_likes", blank=True)
    project_description = models.TextField(help_text="What is this project about?")
    short_description_for_project = models.CharField(max_length=100, default="This is an awesome project")
    views = models.IntegerField(default=0, blank=True)
    project_logo = models.ImageField(upload_to="project_logos", blank=True, default="project-logo-default.png")
    project_status = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title

    def get_absolute_project_url(self):
        return reverse("project_detail", args={self.project_title})


class ProjectFiles(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_making_contribution")
    file_name = models.CharField(max_length=100)
    code = models.TextField(help_text="Enter your code here.")
    approves = models.ManyToManyField(User, related_name="those_who_approved", blank=True)
    approved = models.BooleanField(default=False, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    def get_absolute_project_file(self):
        return reverse("project_file_detail", args={self.pk})


class Issues(models.Model):
    projectF = models.ForeignKey(ProjectFiles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issues = models.TextField(help_text="What are the issues about this code?Just address the issue without fix")
    fix = models.TextField("What should be the fix?Provide it here.")
    resolved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} just highlighted an issue in {self.projectF.file_name}"


class ProjectIssues(models.Model):
    project_with_issue = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.CharField(max_length=50, help_text="What are the issues about this project?", default="There is a "
                                                                                                          "typo in "
                                                                                                          "one of the "
                                                                                                          "project "
                                                                                                          "files")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} just addressed an issue about {self.project_with_issue.project_title}"

    def get_absolute_projectissue(self):
        return reverse("project_issue_detail", args={self.pk})


class FixProjectIssue(models.Model):
    issue = models.ForeignKey(ProjectIssues, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fix = models.CharField(max_length=350, help_text="What should be the fix?Provide it here.")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} added a fix to {self.issue.project_with_issue}"


class NotifyMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify_title = models.CharField(max_length=100, default="New Notification")
    notify_alert = models.CharField(max_length=200)
    follower_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="who_started_following")
    read = models.BooleanField(default=False)
    date_notified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New {self.notify_title} to {self.user}"

    def get_absolute_notification_url(self):
        return reverse("notify_detail", args=self.pk)


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500, help_text="your suggestions are important,let us know. ")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} gave a feedback"


class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} wrote {self.subject}"
