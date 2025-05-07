from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),

    # Job URLs
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),

    # Skill URLs
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    path('skills/create/', views.SkillCreateView.as_view(), name='skill_create'),
    path('skills/<int:pk>/update/', views.SkillUpdateView.as_view(), name='skill_update'),
    path('skills/<int:pk>/delete/', views.SkillDeleteView.as_view(), name='skill_delete'),

    # Candidate URLs
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    path('candidates/create/', views.CandidateCreateView.as_view(), name='candidate_create'),
    path('candidates/<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),
    path('candidates/<int:pk>/update/', views.CandidateUpdateView.as_view(), name='candidate_update'),
    path('candidates/<int:pk>/edit/', views.CandidateUpdateView.as_view(), name='candidate_edit'),  # Alias for update
    path('candidates/<int:pk>/delete/', views.CandidateDeleteView.as_view(), name='candidate_delete'),
]