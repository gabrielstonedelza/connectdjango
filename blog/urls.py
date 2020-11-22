from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as uviews
urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
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
    path('blogs/',views.blogs,name='blogs'),
    path("blog/new/", views.create_blog, name="create_blog"),
    path('blog/<str:title>/',views.blog_detail,name='blog_detail'),
    path('blog/<str:title>/update/',views.blog_update,name='blog_update'),
    path('like_blog/<str:title>/', views.like_blog,name='like_blog'),
    path('chat/',views.chatrooms,name="chatrooms"),
    path('chat/<str:room_name>/', views.room_detail, name='room_detail'),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('about-us/', views.about_cd, name="about-us"),

    path('notifications/', views.user_notifications, name='notifications'),

    path('search/', views.search_queries, name='search'),
    path('<str:username>/following/', views.user_profile_following, name="deuser_followings"),
    path('<str:username>/followers/', views.user_profile_followers, name="deuser_followers"),
    path('<str:username>/', views.user_profile, name="userprofilepost"),

]
