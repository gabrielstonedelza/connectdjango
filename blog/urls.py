from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as uviews

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('register/', uviews.register, name='register'),
    path('tutorial/new/', views.create_tutorial, name="tutorial_new"),
    path('tutorials/', views.all_tutorial, name='tutorials'),
    path('tutorial/<int:id>/', views.tutorial_detail, name="tutorial_detail"),
    path('like-tutorial/<int:id>/', views.like_tutorial, name="tutorial_like"),
    path('blog-posts/', views.blogs, name="all_blogs"),
    path('blog-post/<int:id>/', views.blog_detail, name="blogpost_detail"),
    path('like-blog/<int:id>/', views.like_blog, name="like_blog"),
    path("blog/new/", views.create_blog, name="create_blog"),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('contact-us/', views.contact_us, name="contact-us"),
    path('about-us/', views.about_cd, name="about-us"),

    path('notifications/', views.user_notifications, name='notifications'),

    path('search/', views.search_queries, name='search'),
    path('<str:username>/', views.user_profile, name="userprofilepost"),

]
