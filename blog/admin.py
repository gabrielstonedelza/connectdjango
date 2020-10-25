from django.contrib import admin
from .models import (Tutorial, Comments, NotifyMe, FeedBack, ContactUs, BlogPost)

admin.site.register(Tutorial)
admin.site.register(Comments)
admin.site.register(BlogPost)

admin.site.register(NotifyMe)
admin.site.register(FeedBack)
admin.site.register(ContactUs)
