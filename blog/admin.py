from django.contrib import admin
from .models import (Tutorial, Comments, NotifyMe, FeedBack, BlogPost, ImproveTuto, ImproveTutoComments)

admin.site.register(Tutorial)
admin.site.register(Comments)
admin.site.register(BlogPost)
admin.site.register(ImproveTuto)
admin.site.register(ImproveTutoComments)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
