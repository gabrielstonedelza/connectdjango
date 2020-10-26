from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include("blog.urls")),
                  path('oauth/', include('social_django.urls', namespace='social')),
                  
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
                  path('profile/<str:username>/', user_views.profile, name='profile'),
                  path('profile/<str:username>/following/', user_views.profile_followings, name="pfollowing"),
                  path('profile/<str:username>/followers/', user_views.profile_followers, name="pfollowers"),
                  path('connection/<int:id>/', user_views.user_connection, name='connection'),
                  path('profile_following/<int:id>/', user_views.profile_following, name='profile_following'),
                  path('profile_connection_followers/<int:id>/', user_views.profile_connection_followers,
                       name='profile_connection_followers'),
                  path('<str:username>/edit/', user_views.edit_profile, name="editprofile"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
