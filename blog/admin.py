from django.contrib import admin
from .models import (ChatRoom,Message,PrivateMessage, NotifyMe, FeedBack)

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
