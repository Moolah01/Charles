from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  index, register, login_view, student_dashboard_view, teacher_dashboard_view
from .admin import custom_admin_site  # Import the custom admin site
from . import views  # Add this import
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Custom Admin page
    path('custom_admin/', custom_admin_site.urls, name='custom_admin'),  # Ensure the name='custom_admin' is defined

    # Home page
    path('', index, name='index'),

    # Student dashboard page
    path('student-dashboard/', student_dashboard_view, name='student-dashboard'),

    # Teacher dashboard page
    path('teacher-dashboard/', teacher_dashboard_view, name='teacher-dashboard'),

    # User registration page
    path('register/', register, name='register'),

    # Login using custom login view
    path('login/', login_view, name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset views
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset_form.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name='password_reset_complete'),
    # Add these to your existing urlpatterns
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    # Change the reference in the URL pattern from views.teacher_dashboard to views.teacher_dashboard_view
    path('teacher-dashboard/', views.teacher_dashboard_view, name='teacher-dashboard'),
    path('profile_teacher/', views.profile_teacher, name='profile_teacher'),
    path('edit-profile-teacher/', views.edit_profile_teacher, name='edit_profile_teacher'),
    path('change-password-teacher/', views.change_password_teacher, name='change_password_teacher'),
    path('delete-account-teacher/', views.delete_account_teacher, name='delete_account_teacher'),

    #Manage_class
    path('create_class/', views.create_class, name='create_class'),
    path('invite_student/<int:class_id>/', views.invite_student_to_class, name='invite_student_to_class'),
    path('class_list/', views.class_list, name='class_list'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('accept_invitation/<int:invitation_id>/', views.accept_invitation, name='accept_invitation')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)