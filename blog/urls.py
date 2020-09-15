from django.urls import path

from . import views
from .views import TutorialDeleteView
from django.contrib.auth import views as auth_views
from users import views as uviews
from users.views import CreateNewGroupView

urlpatterns = [
    path('', views.login_request, name="login"),
    path('register/', uviews.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('logout/', uviews.logout_request, name='logout'),
    path('latest_qs/', views.latest_qs, name='latest_questions'),
    path('most_answered_qs/', views.answered_questions, name='most_answered_questions'),
    path('unanswered_qs/', views.unanswered_qs, name='unanswered_questions'),
    path('latest_tutos/', views.latest_tutorials, name='latest_tutorials'),
    path('most_viewed_tutos/', views.most_viewed_tutorials, name='most_viewed_tutorials'),
    path('locked_tutos/', views.locked_tutorials, name='loked_tutorials'),

    path('feedbacks/', views.feed_backs, name="feedbacks"),
    path('contact-us/', views.contact_us, name="contact-us"),
    path('about-us/', views.about_cd, name="about-us"),

    path('groups/', uviews.all_groups, name='groups'),
    path('group_posts/', uviews.all_groups_posts, name='group_posts'),
    path('group/new/', CreateNewGroupView.as_view(), name='group-create'),
    path('group/update/', uviews.group_update, name='group_update'),
    path('remove_member/<int:id>/', uviews.remove_member, name='remove_member'),
    path('invite_members/<int:id>/', uviews.join_group, name='invite_members'),
    path('add_pending_members/<int:id>/', uviews.add_pending_members, name='add_pending_members'),
    path('join_group/<int:id>/', uviews.join_group, name='join_group'),

    path('notifications/', views.user_notifications, name='notifications'),
    path('group/<int:id>/', uviews.group_detail, name='group_detail'),
    path('group_post/<int:id>/', uviews.group_post_detail, name="group_post_detail"),
    path('like_gpost/<int:id>/', uviews.like_group_post, name="like_gpost"),
    path('question/<int:id>/', views.question_detail, name='question_detail'),

    path('tutorials/', views.all_tutorials, name='tutorials'),
    path('tutorial/<int:id>/', views.tutorial_detail, name='tuto_detail'),
    path('tutorial/<int:id>/update/', views.update_tutorial, name='tutorial_update'),
    path('tutorial/<int:pk>/delete/', TutorialDeleteView.as_view(), name='tutorial_delete'),
    path('question/new/', views.create_question, name='question-create'),
    path('tutorial/new/', views.create_tutorial, name='tutorial-create'),
    path('like_tutorial/<int:id>/', views.like_tutorial, name='like_tutorial'),

    path('question/new/', views.create_question, name='question-create'),
    path('tutorial/new/', views.create_tutorial, name='tutorial-create'),

    path('search/', views.search_queries, name='search'),
    path('explore/', views.explore_new, name='explore'),
    path('new2dja/', views.new_to_dja, name='new2dja'),
    path('<str:username>/', views.user_post_profile, name="userprofilepost"),

]
