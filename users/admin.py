from django.contrib import admin

from .models import (Profile, Group, GroupPost, LoginConfirmCode, GroupAdminMsg, LastSeen, Comments)

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(GroupPost)
admin.site.register(LoginConfirmCode)
admin.site.register(GroupAdminMsg)
admin.site.register(LastSeen)
admin.site.register(Comments)

