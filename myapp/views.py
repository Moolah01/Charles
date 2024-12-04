from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import RegisterForm  # Your custom register form (ensure it has a 'role' field)
from django.shortcuts import render, get_object_or_404
from .models import Class, Quiz, CustomUser
from .forms import ClassForm, InviteStudentForm
from .models import Invitation, ClassEnrollment
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from .models import Quiz, Question, Option
from .forms import QuizForm, QuestionForm, OptionForm
from django.http import HttpResponse
import csv
from django.http import JsonResponse



# Home page
def index(request):
    return render(request, "myapp/index.html")

# Custom Admin page (for admin users)
def custom_admin(request):
    return render(request, 'myapp/custom_admin.html')

# Student Dashboard view (requires login)
# @login_required
# def student_dashboard_view(request):
#     return render(request, 'myapp/student-dashboard.html')


# Change the name of this function from teacher_dashboard_view to teacher_dashboard
@login_required
def teacher_dashboard_view(request):
    return render(request, 'myapp/teacher_dashboard.html')

# Registration view (redirecting based on role)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            role = form.cleaned_data.get('role')  # Capture the selected role from the form

            # If the user is a superuser, skip assigning a role
            if user.is_superuser:
                role = None  # Superuser does not have a role

            user.save()  # Save any changes (if any role changes)

            # Log the user in automatically after registration
            login(request, user)

            # Redirect based on user role
            if role == 'teacher':
                return redirect('teacher-dashboard')  # Redirect to the teacher dashboard
            elif role == 'student':
                return redirect('student-dashboard')  # Redirect to the student dashboard
            else:
                return redirect('admin')  # Redirect to an admin dashboard or homepage for superusers
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()  # If the request is GET, just render the form

    return render(request, 'myapp/register.html', {'form': form})

# Login view with error message
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on user role or admin status
                if user.is_superuser:
                    return redirect('/admin/')  # Redirect to the default Django admin page
                elif hasattr(user, 'role') and user.role == 'teacher':
                    return redirect('teacher-dashboard')  # Redirect to the teacher dashboard
                else:
                    return redirect('student-dashboard')  # Redirect to the student dashboard (default)
            else:
                error_message = "Incorrect username or password."
        else:
            error_message = "Incorrect username or password."  # Message for invalid form
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form, 'error_message': error_message})

# Edit Profile view (Allow users to update their details)
@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')  # Getting the profile picture

        try:
            # Update the user's details
            user.username = username
            user.email = email
            if profile_picture:
                user.profile_picture = profile_picture  # Set the new profile picture if uploaded
            user.save()

            # Success message
            messages.success(request, 'Profile updated successfully!')

            return redirect('profile')  # Redirect to profile page or wherever appropriate
        except Exception as e:
            # In case of any error, show an error message
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('edit_profile')

    return render(request, 'edit_profile.html')  # Render the edit profile form if GET request

# Delete Account view
@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()  # Delete the current user
        return redirect('index')  # Redirect to the home page after account deletion
    return render(request, 'myapp/delete_account.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "The new passwords do not match.")
            return redirect('change_password')  # Adjust this URL name accordingly

        # Check if old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('change_password')

        # Update password
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep the user logged in after changing the password

        messages.success(request, "Your password has been successfully updated.")
        return redirect('profile')  # Redirect to the profile page or wherever you want

    return render(request, 'change_password.html')  # Optionally, you can have a separate page for it

# Profile view
@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

# Teacher Profile view
@login_required
def profile_teacher(request):
    return render(request, 'myapp/profile_teacher.html')

# Edit Teacher Profile
@login_required
def edit_profile_teacher(request):
    if request.method == "POST":
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        try:
            # Update teacher's details
            user.username = username
            user.email = email
            if profile_picture:
                user.profile_picture = profile_picture
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_teacher')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('edit_profile_teacher')

    return render(request, 'edit_profile_teacher.html')

@login_required
def change_password_teacher(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            messages.error(request, "The new passwords do not match.")
            return redirect('change_password_teacher')

        # Check if the new password is the same as the old password
        if old_password == new_password:
            messages.error(request, "The new password cannot be the same as the old password.")
            return redirect('change_password_teacher')

        # Verify the old password
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('change_password_teacher')

        # Set the new password and save it
        request.user.set_password(new_password)
        request.user.save()

        # Debugging: Check the user object after saving
        print(f"User object after password change: {request.user}")

        # Update the session to keep the user logged in with the new password
        update_session_auth_hash(request, request.user)

        # Debugging: Ensure the session is updated
        print(f"Session updated for user: {request.user}")

        messages.success(request, "Your password has been successfully updated.")
        return redirect('profile_teacher')

    return render(request, 'change_password_teacher.html')

# Delete Teacher Account
@login_required
def delete_account_teacher(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('profile_teacher')  # Redirect to the home page after account deletion
    return render(request, 'myapp/delete_account_teacher.html')


#New-----------------------------------------------------------------------
@login_required
def manage_classes(request):
    classes = Class.objects.filter(teacher=request.user)  # Fetch classes created by the teacher
    create_class_form = ClassForm()  # Form for creating a new class
    invite_student_form = InviteStudentForm()  # Form for inviting students

    return render(request, 'manage-class/manage_classes.html', {
        'classes': classes,  # Pass class list to template
        'form': create_class_form,  # Pass create class form to template
        'invite_student_form': invite_student_form,  # Pass invite student form to template
    })

#Create class
@login_required
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = request.user
            new_class.save()
            return redirect('manage_classes')  # Redirect back to the Manage Classes page
    return redirect('manage_classes')

@login_required
def invite_student(request, class_id):
    # Fetch the class to ensure the teacher owns it
    class_instance = get_object_or_404(Class, id=class_id, teacher=request.user)

    if request.method == 'POST':
        form = InviteStudentForm(request.POST)
        if form.is_valid():
            student_username = form.cleaned_data['student_username']

            try:
                # Fetch the student user
                student = CustomUser.objects.get(username=student_username, role='student')

                # Check if an invitation already exists
                if Invitation.objects.filter(student=student, class_invited=class_instance).exists():
                    messages.warning(request, f"An invitation has already been sent to {student_username}.")
                else:
                    # Create a new invitation
                    Invitation.objects.create(
                        teacher=request.user,
                        student=student,
                        class_invited=class_instance
                    )
                    messages.success(request, f"Invitation sent to {student_username}!")
            except CustomUser.DoesNotExist:
                # If no user is found
                messages.error(request, f"No student found with username '{student_username}'.")

    # Redirect back to manage classes
    return redirect('manage_classes')

# #Take quiz
# @login_required
# def take_quiz(request, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     if request.user not in quiz.assigned_class.students.all():
#         return HttpResponseForbidden("You are not allowed to take this quiz.")

#Student dashboard fetch-------
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('index')  # Restrict access to students only

    # Fetch enrolled classes for the logged-in student
    enrolled_classes = request.user.enrolled_classes.all()  # Uses the ManyToMany relationship

    # Fetch pending invitations
    invitations = Invitation.objects.filter(student=request.user, is_accepted=False)

    return render(request, 'myapp/student-dashboard.html', {
        'enrolled_classes': enrolled_classes,
        'invitations': invitations,
    })


@login_required
def student_invitations(request):
    student = request.user

    # Fetch all pending invitations for the logged-in student
    invitations = Invitation.objects.filter(student=student, is_accepted=False)

    return render(request, 'manage-class/student_invitations.html', {'invitations': invitations})


@login_required
def accept_invitation(request, username):
    # Ensure the logged-in user is the student accepting the invitation
    if request.user.username != username:
        return HttpResponseForbidden("You cannot accept invitations for another user.")

    student = request.user

    # Get the latest pending invitation for the student
    invitation = Invitation.objects.filter(student=student, is_accepted=False).order_by('-date_sent').first()

    if not invitation:
        messages.error(request, "No pending invitations found.")
        return redirect('student-invitations')  # Redirect back to invitations if none are found

    if request.method == 'POST':
        # Mark the invitation as accepted
        invitation.is_accepted = True
        invitation.save()

        # Add the student to the class
        invitation.class_invited.students.add(student)

        # Display a success message
        messages.success(request, f"You have successfully joined the class: {invitation.class_invited.name}")

        # Redirect back to the invitations page
        return redirect('student-invitations')

    # Redirect back to the invitations page for non-POST requests
    return redirect('student-invitations')


@login_required
def student_class_details(request, class_id):
    # Ensure the student is enrolled in the class
    class_instance = get_object_or_404(Class, id=class_id, students=request.user)

    return render(request, 'manage-class/student_class_details.html', {
        'class_instance': class_instance,
    })

@login_required
def class_details(request, class_id):
    # Fetch the specific class and its students
    class_instance = get_object_or_404(Class, id=class_id, teacher=request.user)
    students = class_instance.students.all()  # Get all enrolled students

    return render(request, 'manage-class/class_details.html', {
        'class_instance': class_instance,
        'students': students
    })

@login_required
def enrolled_classes(request):
    student = request.user

    # Fetch all classes where the student is enrolled
    classes = student.enrolled_classes.all()  # Uses the related_name 'enrolled_classes'

    return render(request, 'manage-class/enrolled_classes.html', {'classes': classes})

#New-----------------------------------------------------------------------------
def delete_class(request, class_id):
    """Handles class deletion."""
    if request.method == "POST":
        class_to_delete = get_object_or_404(Class, id=class_id, teacher=request.user)
        class_to_delete.delete()  # Delete the class
        messages.success(request, "Class deleted successfully!")
    return redirect('manage_classes')  # Redirect back to the Manage Classes page

#Quiz Bago------------------------------------------------------------------------------
@login_required
def simple_manage_classes(request):
    # Simpler version just fetching and showing classes
    teacher_classes = Class.objects.filter(teacher=request.user)
    return render(request, 'manage-class/manage_classes.html', {'classes': teacher_classes})


def manage_quizzes(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    quizzes = Quiz.objects.filter(assigned_class=class_obj)
    return render(request, 'manage-class/manage_quizzes.html', {'class': class_obj, 'quizzes': quizzes})

@login_required
def create_quiz(request, class_id):
    assigned_class = get_object_or_404(Class, id=class_id)
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.assigned_class = assigned_class
            quiz.save()
            return redirect('manage_quizzes', class_id=class_id)
    else:
        form = QuizForm()
    return render(request, 'manage-class/create_quiz.html', {'form': form, 'class': assigned_class})

def edit_quiz(request):
    """
    Handles editing a quiz.
    - Fetches the quiz object using the provided quiz_id.
    - Updates the quiz using the data from the submitted form.
    - Redirects back to the 'manage_quizzes' page or displays errors if the form is invalid.
    """
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')  # Get the quiz ID from the form
        quiz = get_object_or_404(Quiz, id=quiz_id)  # Fetch the quiz object

        # Bind the form with the submitted data and the quiz instance
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()  # Save the updated quiz object
            # Redirect to the 'manage_quizzes' page with the class ID
            return redirect('manage_quizzes', class_id=quiz.assigned_class.id)
        else:
            # If the form is invalid, render the page with errors
            return render(request, 'manage-class/manage_quizzes.html', {
                'quizzes': Quiz.objects.filter(assigned_class=quiz.assigned_class),  # List of quizzes for the class
                'form': form,  # Return the form with validation errors
                'class': quiz.assigned_class,  # Pass the class for context
            })
    # If the request is invalid (e.g., not POST), redirect to the 'manage_classes' page
    return redirect('manage_classes')

def delete_quiz(request):
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')  # Get the quiz ID from the form
        quiz = get_object_or_404(Quiz, id=quiz_id)  # Fetch the quiz object

        # Save the assigned class ID for redirection
        assigned_class_id = quiz.assigned_class.id
        quiz.delete()  # Delete the quiz

        # Redirect to the 'manage_quizzes' page for the associated class
        return redirect('manage_quizzes', class_id=assigned_class_id)
    # If the request is invalid (e.g., not POST), redirect to the 'manage_classes' page
    return redirect('manage_classes')

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = OptionForm(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            for form in formset:
                option = form.save(commit=False)
                option.question = question
                option.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuestionForm()
        formset = OptionForm()
    return render(request, 'manage-class/add_questions.html', {'form': form, 'formset': formset, 'quiz': quiz})

@login_required
def download_grades(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}_grades.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Grade'])

    # Example: Fetch grades from quiz results
    for student in quiz.assigned_class.students.all():
        # Replace with actual grade logic
        writer.writerow([student.username, 'Grade Placeholder'])

    return response

#New-------------------------------------------------------------
def available_quizzes(request, class_id):
    quizzes = Quiz.objects.filter(assigned_class_id=class_id)
    return render(request, 'take-quiz/quizzes.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Fetch all questions for the quiz
    return render(request, 'take-quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer and user_answer.strip().lower() == question.correct_answer.strip().lower():
                score += 1

        # Calculate percentage score
        percentage_score = (score / total_questions) * 100

        # Save the result if needed (e.g., QuizSubmission model)
        return JsonResponse({'score': score, 'percentage': percentage_score})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
