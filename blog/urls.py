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
    path('newsletter/', views.news_letter, name='newsletter'),
    path('tutorial/new/', views.create_tutorial, name="tutorial_new"),
    path('tutorials/', views.all_tutorial, name='tutorials'),
    path('tutorial/<int:id>/', views.tutorial_detail, name="tutorial_detail"),
    path('tutorial/improvement/<int:id>/', views.tutorial_improvements, name="improve_tuto_detail"),
    path('like-tutorial/<int:id>/', views.like_tutorial, name="tutorial_like"),
    path('tutorial/<int:id>/update/', views.update_tutorial, name='tutorial_update'),
    path('blog-posts/', views.blogs, name="all_blogs"),
    path("blog/new/", views.create_blog, name="create_blog"),
    path('blog-post/<int:id>/', views.blog_detail, name="blogpost_detail"),
    path('like-blog/<int:id>/', views.like_blog, name="like_blog"),
    path('blog/<int:id>/update/', views.update_blog, name='blog_update'),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('about-us/', views.about_cd, name="about-us"),

    path('notifications/', views.user_notifications, name='notifications'),

    path('search/', views.search_queries, name='search'),
    path('<str:username>/following/', views.user_profile_following, name="deuser_followings"),
    path('<str:username>/followers/', views.user_profile_followers, name="deuser_followers"),
    path('<str:username>/', views.user_profile, name="userprofilepost"),

]
