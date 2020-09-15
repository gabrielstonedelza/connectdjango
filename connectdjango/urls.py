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
      path('profile/<str:username>/', user_views.profile, name='profile'),
      path('connection/<int:id>/', user_views.user_connection, name='connection'),
      path('profile_following/<int:id>/', user_views.profile_following, name='profile_following'),
      path('profile_connection_followers/<int:id>/', user_views.profile_connection_followers,
           name='profile_connection_followers'),
      path('<str:username>/edit/', user_views.edit_profile, name="editprofile"),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)