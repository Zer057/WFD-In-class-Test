# recruiting/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # Include other app URLs
    path('jobs/', include('jobs.urls')),
    path('applications/', include('applications.urls')),
    path('skills/', include('skills.urls')),

    # Add recruiting-specific URLs here
    # Example: path('dashboard/', views.dashboard, name='dashboard'),
]