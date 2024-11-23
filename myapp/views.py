from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ClassForm
from .models import Invitation
from .models import CustomUser  # Import CustomUser model
from .forms import RegisterForm  # Your custom register form (ensure it has a 'role' field)
from django.shortcuts import render, get_object_or_404
from .models import Class


# Home page
def index(request):
    return render(request, "myapp/index.html")

# Custom Admin page (for admin users)
def custom_admin(request):
    return render(request, 'myapp/custom_admin.html')

# Student Dashboard view (requires login)
@login_required
def student_dashboard_view(request):
    return render(request, 'myapp/student-dashboard.html')


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


def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')  # Adjust this to your desired redirect
    else:
        form = ClassForm()

    return render(request, 'manage-class/create_class.html', {'form': form})


def invite_student_to_class(request, class_id):
    # Your logic for inviting a student to a class
    class_instance = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        # Handle the form submission and invitation logic here
        pass

    return render(request, 'manage-class/invite_student.html', {'class_instance': class_instance})


def class_list(request):
    # Fetch all classes or perform any required logic
    classes = Class.objects.all()  # Assuming you have a 'Class' model
    return render(request, 'manage-class/class_list.html', {'classes': classes})

def class_detail(request, class_id):
    # Retrieve the specific class based on the class_id from the URL
    class_instance = get_object_or_404(Class, id=class_id)
    return render(request, 'manage-class/class_detail.html', {'class_instance': class_instance})

def accept_invitation(request, token):
    # Retrieve the invitation based on the unique token
    invitation = get_object_or_404(Invitation, token=token)

    # Update the invitation status to accepted
    invitation.accepted = True
    invitation.save()

    # Redirect the user to a confirmation page or wherever appropriate
    return redirect('class_list')  # Adjust this to your desired redirect path