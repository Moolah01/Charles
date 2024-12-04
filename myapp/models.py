from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils.timezone import now

created_at = models.DateTimeField(auto_now_add=True, default=now)

# Custom User model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name="User Role"
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Email Confirmed"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True, blank=True,
        verbose_name="Profile Picture"
    )

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
        verbose_name="User Groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
        verbose_name="User Permissions"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['id']

#New-------------------------------------------------------------
class Class(models.Model):
    name = models.CharField(max_length=255, verbose_name="Class Name")
    description = models.TextField(blank=True, null=True, verbose_name="Class Description")
    teacher = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name="Teacher"
    )
    max_students = models.PositiveIntegerField(default=30, verbose_name="Maximum Students")
    students = models.ManyToManyField(
        'CustomUser',
        related_name='enrolled_classes',
        blank=True,
        verbose_name="Students"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Invitation Model
class Invitation(models.Model):
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
        verbose_name="Teacher"
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_invitations',
        verbose_name="Student"
    )
    class_invited = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='invitations',
        verbose_name="Class Invited"
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name="Invitation Accepted"
    )
    date_sent = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Sent"
    )

    def __str__(self):
        return f"Invitation to {self.student.username} for {self.class_invited.name} by {self.teacher.username}"

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        ordering = ['-date_sent']

class ClassEnrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    is_accepted = models.BooleanField(default=False)  # Field to mark accepted classes
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.enrolled_class.name}"

#Quiz New----------------------------------------------------------
#Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_class = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='quizzes')
    schedule = models.DateTimeField()  # Date and time of the quiz
    timer = models.PositiveIntegerField(help_text="Time limit in minutes")  # Timer for the quiz
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('TF', 'True or False'),
        ('ID', 'Identification'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')  # Add this relationship
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    correct_answer = models.TextField()

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # Identify the correct answer for MCQs

    def __str__(self):
        return self.text


