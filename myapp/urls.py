from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  index, register, login_view,  teacher_dashboard_view
from .admin import custom_admin_site  # Import the custom admin site
from . import views  # Add this import
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Custom Admin page
    path('custom_admin/', custom_admin_site.urls, name='custom_admin'),  # Ensure the name='custom_admin' is defined

    # Home page
    path('', index, name='index'),

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
    path('profile_teacher/', views.profile_teacher, name='profile_teacher'),
    path('edit-profile-teacher/', views.edit_profile_teacher, name='edit_profile_teacher'),
    path('change-password-teacher/', views.change_password_teacher, name='change_password_teacher'),
    path('delete-account-teacher/', views.delete_account_teacher, name='delete_account_teacher'),

    #New--------------------------------------------------------------------------
    path('classes/', views.manage_classes, name='manage_classes'),
    path('classes/create/', views.create_class, name='create_class'),
    path('classes/<int:class_id>/invite/', views.invite_student, name='invite_student'),
    path('invitations/', views.student_invitations, name='student-invitations'),
    path('invitations/<str:username>/accept/', views.accept_invitation, name='accept_invitation'),
    path('classes/<int:class_id>/details/', views.class_details, name='class_details'),
    path('classes/<int:class_id>/details/', views.student_class_details, name='student_class_details'),
    path('enrolled-classes/', views.enrolled_classes, name='enrolled-classes'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),

    #new-------------------------------------------------------------------------
    path('manage-classes/', views.manage_classes, name='manage_classes'),
    path('create-class/', views.create_class, name='create_class'),
    path('classes/<int:class_id>/invite/', views.invite_student, name='invite_student'),
    path('delete-class/<int:class_id>/', views.delete_class, name='delete_class'),

    #Quiz------------------------------------------------------------------------------------
    path('classes/<int:class_id>/quizzes/create/', views.create_quiz, name='create_quiz'),
    path('classes/<int:class_id>/quizzes/', views.manage_quizzes, name='manage_quizzes'),
    path('quizzes/edit/', views.edit_quiz, name='edit_quiz'),
    path('quizzes/delete/', views.delete_quiz, name='delete_quiz'),
    path('quizzes/<int:quiz_id>/add_questions/', views.add_questions, name='add_questions'),
    path('quizzes/<int:quiz_id>/download_grades/', views.download_grades, name='download_grades'),

    #Take-quiz student--------------------------------------------------------------------------
    path('class/<int:class_id>/quizzes/', views.available_quizzes, name='available_quizzes'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)