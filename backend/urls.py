from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),  # API endpoints
    path('', include('library.frontend_urls')),  # Frontend route
]