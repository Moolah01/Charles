from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your CustomUser model
from .models import Class, Quiz, QuizAttempt

# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"  # Custom header for the admin site
    site_title = "Admin Portal"  # Custom title for the admin portal
    index_title = "Welcome to the Administration Portal"  # Title for the index page

    # Optionally include a custom CSS file for styling
    def each_context(self, request):
        context = super().each_context(request)
        context['css_file'] = 'admin/css/custom_admin.css'  # Reference a custom CSS file
        return context

# Instantiate the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser  # Specify the model to customize
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role and Status', {'fields': ('role', 'is_confirmed', 'is_staff', 'is_active')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    # Custom queryset to filter out superusers with 'student' role
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(role='student', is_superuser=True)  # Exclude superusers with 'student' role
        return queryset

# Register the CustomUser model with the default admin site
admin.site.register(CustomUser, CustomUserAdmin)

# Alternatively, register the CustomUser model with your custom admin site
custom_admin_site.register(CustomUser, CustomUserAdmin)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'max_students']
    search_fields = ['name', 'teacher__username']
    list_filter = ['teacher']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_assigned', 'total_questions', 'max_attempts']
    search_fields = ['title', 'class_assigned__name']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'attempts', 'score']
    search_fields = ['student__username', 'quiz__title']


