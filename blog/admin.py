from django.contrib import admin
from .models import (ChatRoom,Message,PrivateMessage, NotifyMe, FeedBack,Blog, Comments,LoginConfirmCode)

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
admin.site.register(Comments)
admin.site.register(LoginConfirmCode)
admin.site.register(Blog)
