import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

class Tutorial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="tutorial_images", help_text="just a photo to simplify what you are teaching.",
                              blank=True)
    tutorial_content = models.TextField(help_text="Type tutorial here")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    views = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        

    def likes_count(self):
        return self.likes.count

    def get_absolute_url(self):
        return reverse("tutorial_detail", args={self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 900:
                output_size = (680, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Comments(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

class ImproveTuto(models.Model):
    tuto = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, default="")
    views = models.IntegerField(default=0)
    can_be_modified = models.TextField(help_text="Which or part of this tutorial can be improved or changed?")
    improvement_or_change = models.TextField(help_text="What is your modification?")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tuto.title

    def get_absolut_improvement(self):
        return reverse("improve_tuto_detail",args={self.pk})


class ImproveTutoComments(models.Model):
    improvetutocomment = models.ForeignKey(ImproveTuto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.improvetutocomment.title

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


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    blog_image = models.ImageField(upload_to="blog_images", help_text="A photo to illustrate your post.", blank=True)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)
    views = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_blog_post(self):
        return reverse("blogpost_detail", args={self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.blog_image:
            img = Image.open(self.blog_image.path)

            if img.height > 400 or img.width > 700:
                output_size = (680, 400)
                img.thumbnail(output_size)
                img.save(self.blog_image.path)

    def likes_count(self):
        return self.likes.count


class NotifyMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify_title = models.CharField(max_length=100, default="New Notification")
    notify_alert = models.CharField(max_length=200)
    follower_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="who_started_following")
    read = models.BooleanField(default=False)
    blog_id = models.IntegerField(blank=True, default=0)
    tuto_id = models.IntegerField(blank=True, default=0)
    improvement_id = models.IntegerField(blank=True, default=0)
    date_notified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New {self.notify_title} notification sent to  {self.user}"

    def get_absolute_notification_url(self):
        return reverse("notify_detail", args=self.pk)
