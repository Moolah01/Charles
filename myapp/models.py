from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


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


class Class(models.Model):
    name = models.CharField(max_length=255, verbose_name="Class Name")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classes',
                                verbose_name="Teacher")
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_classes', blank=True,
                                      verbose_name="Students")
    max_students = models.PositiveIntegerField(default=30, verbose_name="Max Number of Students")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

class Quiz(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='quizzes', verbose_name="Assigned Class")
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    total_questions = models.PositiveIntegerField(verbose_name="Total Questions")
    max_attempts = models.PositiveIntegerField(default=1, verbose_name="Max Attempts per Student")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Student")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Quiz")
    attempts = models.PositiveIntegerField(default=0, verbose_name="Number of Attempts")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Score")

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"

# Ensure the Invitation model has student, is_accepted, and any other necessary fields
class Invitation(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assuming CustomUser is your user model
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

