import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=150, help_text="Title of your project")
    contributors = models.ManyToManyField(User, related_name="wants_to_contribute",
                                          help_text="Invite other users to help build this project with you.")
    project_description = models.TextField(help_text="What is this project about?")
    views = models.IntegerField(default=0, blank=True)
    project_status = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} has created a new project"

    def get_absolute_project_url(self):
        return reverse("project_detail", args={self.project_title})


class ProjectFiles(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_making_contribution")
    file_name = models.CharField(max_length=100)
    code = models.TextField(help_text="Use this section if you don't have the file to upload", blank=True)
    code_in_file = models.FileField(upload_to="project_files", help_text="you can leave this field empty if you put "
                                                                         "the code in the code section.", blank=True)
    approves = models.ManyToManyField(User, related_name="those_who_approved")
    approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has made changes to the {self.project.project_title}"

    def get_absolute_project_file(self):
        return reverse("project_file_detail", args={self.file_name})


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
    issues = models.TextField(help_text="What are the issues about this project?Just address the issue without fix")
    fix = models.TextField("What should be the fix?Provide it here.")
    resolved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} just addressed an issue about {self.project_with_issue.project_name}"


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
