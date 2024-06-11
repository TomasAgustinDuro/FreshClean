# backend/urls.py
from django.urls import path, include  
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend_app/', include('backend_app.urls')),  
]
