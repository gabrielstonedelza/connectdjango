from django.contrib import admin
from .models import (Question, Answers, Tutorial, MyLikes, NotifyMe, FeedBack, ContactUs)

admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Tutorial)
admin.site.register(MyLikes)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
admin.site.register(ContactUs)
