from django.contrib import admin
from .models import (Project, ProjectFiles, ProjectIssues, Issues, FixProjectIssue, NotifyMe, FeedBack, ContactUs)

admin.site.register(Project)
admin.site.register(ProjectFiles)
admin.site.register(ProjectIssues)
admin.site.register(Issues)
admin.site.register(FixProjectIssue)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
admin.site.register(ContactUs)
