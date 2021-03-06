from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as uviews

urlpatterns = [

    # path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    # path('', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('register/', uviews.register, name='register'),
    path('newsletter/', views.news_letter, name='newsletter'),
    path('blogs/', views.blogs, name='blogs'),
    path("blog/new/", views.create_blog, name="create_blog"),
    path('blog/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<str:slug>/update/', views.blog_update, name='blog_update'),
    path('like_blog/<str:slug>/', views.like_blog, name='like_blog'),
    path('chat/', views.chat_rooms, name="chatrooms"),
    path('chat/<str:slug>/', views.room_detail, name='room_detail'),
    path('chatroom/new/', views.create_chatroom, name='create_chatroom'),
    path('chatroom/<str:slug>/update/', views.update_room, name='update_chatroom'),
    path('add_pending_members/<int:id>/', views.add_pending_members, name='add_pending_members'),
    path('add_members/<int:id>/', views.add_to_room, name='add_members'),
    path('join_room/<str:slug>/', views.join_room, name='join_room'),
    path('chat/<str:slug>/need-access/', views.need_access, name="need-access"),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('about-us/', views.about_cd, name="about-us"),

    path('notifications/', views.user_notifications, name='notifications'),

    path('search/', views.search_queries, name='search'),
    path('<str:username>/following/', views.user_profile_following, name="deuser_followings"),
    path('<str:username>/followers/', views.user_profile_followers, name="deuser_followers"),
    path('<str:username>/', views.user_profile, name="userprofilepost"),
    # path('direct/inbox/', views.messages, name="messages"),
    # path('direct/<str:chat_id>/', views.private_chat, name='private_chat'),
]
