from django.urls import path

from . import views
from .views import ProjectCreateView
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
    path('projects/', views.all_projects, name='projects'),
    path('new-project/new/', views.ProjectCreateView.as_view(), name="create_project"),
    path('project/<str:project_name>/', views.project_detail, name='project_detail'),
    path('project-file/<int:id>/', views.project_file_detail, name="project_file_detail"),
    path('project/<str:project_name>/issues-fixes/', views.issues_fixes, name="issues_fixes"),
    path('project/<int:id>/files-in/', views.files_in, name="files_in"),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('contact-us/', views.contact_us, name="contact-us"),
    path('about-us/', views.about_cd, name="about-us"),

    path('notifications/', views.user_notifications, name='notifications'),

    path('search/', views.search_queries, name='search'),
    # path('<str:username>/', views.user_post_profile, name="userprofilepost"),

]
