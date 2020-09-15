from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


GROUP_MEMBER_STATUS = (
    ("Pending", "Pending"),
    ("Approved", "Approved")
)

SUPPORTED_FILES = ["docx", "doc", "pdf", "txt", "odt", "rtf", "tex", "wpd", "ods ", "xls", "xlsm", "xlsx", "pptx",
                   "ppt", "pps", "odp"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True, default="I am a django developer")
    name = models.CharField(max_length=150, default="New User")
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, default='default.jpg')
    cover_pic = models.ImageField(upload_to="cover_pics", blank=True, default='cover-default.jpg')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    your_facebook = models.CharField(max_length=450, blank=True)
    your_instagram = models.CharField(max_length=450, blank=True)
    your_twitter = models.CharField(max_length=450, blank=True)
    your_youtube = models.CharField(max_length=450, blank=True)
    your_medium = models.CharField(max_length=450, blank=True)
    your_linkedin = models.CharField(max_length=450, blank=True)
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    def myfollowing_count(self):
        return self.following.count

    def myfollowers_count(self):
        return self.followers.count


class Group(models.Model):
    group_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="group_logos", default="group_default.jpg", blank=True)
    group_description = models.TextField()
    member_status = models.CharField(choices=GROUP_MEMBER_STATUS, default="Pending", max_length=15, blank=True)
    pending_list = models.ManyToManyField(User, related_name='wants_to_join', blank=True)
    members = models.ManyToManyField(User, related_name='group_members', blank=True)
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

    def get_absolute_group_url(self):
        return reverse("group_detail", args={self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail = output_size
            img.save(self.logo.path)


class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    gmember = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_making_post")
    title = models.CharField(max_length=100, default="Likes coding")
    content = models.TextField(default="If you like programming just start learning and start building projects that matter", blank=True)
    photo = models.ImageField(upload_to="group_post_photos", blank=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='group_post_likes', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.group_name} just made a new post"

    def get_absolute_group_post_url(self):
        return reverse("group_post_detail", args={self.pk})

    def likes_count(self):
        return self.likes.count


class Comments(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has commented on {self.post.title}"


class LoginConfirmCode(models.Model):
    logged_user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    logged_in_platform = models.CharField(max_length=100, default="")
    dtime = models.IntegerField(default=30)
    date_logged_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.logged_user.username}"


class LastSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s last seen was {self.last_seen}"


class GroupAdminMsg(models.Model):
    g_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Message to all group members")
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.g_leader} sent a note to all group members"



