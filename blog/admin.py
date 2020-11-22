from django.contrib import admin
from .models import (ChatRoom,Message,PrivateMessage, NotifyMe, FeedBack,Blog, Comments,LoginConfirmCode)

# admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(NotifyMe)
admin.site.register(FeedBack)
admin.site.register(Comments)
admin.site.register(LoginConfirmCode)


@admin.register(Blog)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id','slug')
    prepopulated_fields = { 'slug': ('title',),}

@admin.register(ChatRoom)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'id','slug')
    prepopulated_fields = { 'slug': ('room_name',),}