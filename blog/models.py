import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Group, GroupPost


class Question(models.Model):
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, help_text="Title of your question")
    q_description = models.TextField(default="Someone help me", help_text="Explanation of your question")
    answered = models.BooleanField(default=False, blank=True)
    views = models.IntegerField(default=0, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_author.username} posted '{self.question}'."

    def get_absolute_url(self):
        return reverse("question_detail", args={self.pk})

    def question_count(self):
        return self.question.count


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey("Answers", null=True, related_name="replies", on_delete=models.CASCADE)
    answer = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} answered {self.question}"

    def answers_count(self):
        return self.answer.count


class Tutorial(models.Model):
    tutorial_author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    tutorial_content = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="tutorial_likes", blank=True)
    make_private = models.BooleanField(default=False, help_text="Make this tutorial private")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutorial_author} has posted a tutorial '{self.title}'"

    def get_absolute_tutorial_url(self):
        return reverse("tuto_detail", args={self.pk})

    def likes_count(self):
        return self.likes.count


class MyLikes(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutorial.title}"


class NotifyMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify_title = models.CharField(max_length=100, default="New Notification")
    notify_alert = models.CharField(max_length=200)
    follower_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="who_started_following")
    gname = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    gpost = models.ForeignKey(GroupPost, on_delete=models.CASCADE, blank=True, null=True)
    que_id = models.IntegerField(blank=True, default=0)
    tuto_id = models.IntegerField(blank=True, default=0)
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
