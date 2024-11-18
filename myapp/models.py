from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Choices for the role field
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    # Additional fields
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name="User Role"  # Added for better admin readability
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Email Confirmed"  # Added for better admin readability
    )

    # Add a profile picture field
    profile_picture = models.ImageField(
        upload_to='profile_pics/',  # Directory where images will be stored
        null=True, blank=True,  # Allow the field to be optional
        verbose_name="Profile Picture"
    )

    # Customizing related_name to prevent conflicts with other models using Group and Permission
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Avoids name collision with other user models
        blank=True,
        verbose_name="User Groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Avoids name collision with other user models
        blank=True,
        verbose_name="User Permissions"
    )

    def __str__(self):
        """
        String representation of the CustomUser model for better readability
        in the Django admin and debugging.
        """
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['id']

