from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    # Home/dashboard
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),

    # Candidate URLs
    path('profile/', views.edit_profile, name='edit_profile'),
    path('skills/add/', views.add_skills, name='add_skills'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('applications/', views.my_applications, name='my_applications'),

    # Recruiter URLs
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/skills/<int:skill_id>/', views.candidates_by_skill, name='candidates_by_skill'),
    path('application/<int:application_id>/review/', views.review_application, name='review_application'),
    path('application/<int:application_id>/shortlist/', views.shortlist_candidate, name='shortlist_candidate'),

    # Manager URLs
    path('jobs/pending/', views.pending_jobs, name='pending_jobs'),
    path('jobs/<int:job_id>/approve/', views.approve_job, name='approve_job'),
    path('applications/shortlisted/', views.shortlisted_candidates, name='shortlisted_candidates'),
    path('application/<int:application_id>/assign/', views.assign_interviewer, name='assign_interviewer'),
    path('application/<int:application_id>/finalize/', views.finalize_hiring, name='finalize_hiring'),
]