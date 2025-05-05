from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skills.views import SkillViewSet
from django.http import HttpResponse  # 👈 import for homepage

router = DefaultRouter()
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', lambda request: HttpResponse("Welcome to the Retail Recruitment System")),  # 👈 homepage
]
