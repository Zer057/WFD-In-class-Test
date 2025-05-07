from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Candidate, Job, Skill
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

# -------------------------
# JOB VIEWS
# -------------------------

class HomeView(TemplateView):
    template_name = "candidates/home.html"


class JobListView(ListView):
    model = Job
    template_name = 'candidates/job_list.html'
    context_object_name = 'jobs'

class JobCreateView(PermissionRequiredMixin, CreateView):
    model = Job
    template_name = 'candidates/job_form.html'
    fields = ['title', 'description', 'skills_required']
    success_url = reverse_lazy('job_list')
    permission_required = 'recruitment.add_job'

class JobUpdateView(PermissionRequiredMixin, UpdateView):
    model = Job
    template_name = 'candidates/job_form.html'
    fields = ['title', 'description', 'skills_required']
    success_url = reverse_lazy('job_list')
    permission_required = 'recruitment.change_job'

class JobDeleteView(PermissionRequiredMixin, DeleteView):
    model = Job
    template_name = 'candidates/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')
    permission_required = 'recruitment.delete_job'

# -------------------------
# SKILL VIEWS
# -------------------------

class SkillListView(ListView):
    model = Skill
    template_name = 'candidates/skill_list.html'
    context_object_name = 'skills'

class SkillCreateView(PermissionRequiredMixin, CreateView):
    model = Skill
    template_name = 'candidates/skill_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('skill_list')
    permission_required = 'recruitment.add_skill'

class SkillUpdateView(PermissionRequiredMixin, UpdateView):
    model = Skill
    template_name = 'candidates/skill_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('skill_list')
    permission_required = 'recruitment.change_skill'

class SkillDeleteView(PermissionRequiredMixin, DeleteView):
    model = Skill
    template_name = 'candidates/skill_confirm_delete.html'
    success_url = reverse_lazy('skill_list')
    permission_required = 'recruitment.delete_skill'

# -------------------------
# CANDIDATE VIEWS
# -------------------------

class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidates/candidate_list.html'
    context_object_name = 'candidates'

class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidates/candidate_detail.html'
    context_object_name = 'candidate'

class CandidateCreateView(PermissionRequiredMixin, CreateView):
    model = Candidate
    template_name = 'candidates/candidate_form.html'
    fields = ['user', 'resume']
    success_url = reverse_lazy('candidate_list')
    permission_required = 'recruitment.add_candidate'

class CandidateUpdateView(PermissionRequiredMixin, UpdateView):
    model = Candidate
    template_name = 'candidates/candidate_form.html'
    fields = ['user', 'resume']
    success_url = reverse_lazy('candidate_list')
    permission_required = 'recruitment.change_candidate'

class CandidateDeleteView(PermissionRequiredMixin, DeleteView):
    model = Candidate
    template_name = 'candidates/candidate_confirm_delete.html'
    success_url = reverse_lazy('candidate_list')
    permission_required = 'recruitment.delete_candidate'
