from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
##
from django.http import HttpResponse  # 👈 import for homepage
from rest_framework_simplejwt.views import ( TokenObtainPairView,  TokenRefreshView,)
from django.urls import path
from . import views

router = DefaultRouter()
##router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('', lambda request: HttpResponse("Welcome to the Retail Recruitment System")),  # 👈 homepage
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('jobs.urls')),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]

