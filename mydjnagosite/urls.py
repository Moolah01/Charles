# mydjangosite/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # Default admin site
    path('', include('myapp.urls')),  # Include myapp URLs
]
