# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import User, Candidate, Recruiter, Manager, Job, JobSkill, Application, Interview, Skill, CandidateSkill
from .forms import (
    UserRegisterForm, UserUpdateForm, CandidateUpdateForm, RecruiterUpdateForm,
    ManagerUpdateForm, JobForm, JobSkillFormSet, ApplicationForm, ApplicationReviewForm,
    InterviewForm, SkillForm, CandidateSkillForm
)


# Account Views
def home(request):
    """Home page view"""
    return render(request, 'home.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create profile based on role
            role = form.cleaned_data.get('role')
            if role == 'candidate':
                Candidate.objects.create(user=user)
            elif role == 'recruiter':
                Recruiter.objects.create(user=user)
            elif role == 'manager':
                Manager.objects.create(user=user)

            login(request, user)
            messages.success(request, f'Account created successfully! You are now logged in.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard view based on user role"""
    context = {}
    if request.user.role == 'candidate':
        # Get candidate's applications
        applications = request.user.candidate_profile.applications.all()
        context['applications'] = applications
        # Get available jobs
        context['jobs'] = Job.objects.filter(status='active')
    elif request.user.role == 'recruiter':
        # Get recruiter's posted jobs
        jobs = request.user.recruiter_profile.posted_jobs.all()
        context['jobs'] = jobs
        # Get applications for recruiter's jobs
        applications = Application.objects.filter(job__in=jobs)
        context['applications'] = applications
    elif request.user.role == 'manager':
        # Get pending jobs for approval
        pending_jobs = Job.objects.filter(status='pending_approval')
        context['pending_jobs'] = pending_jobs
        # Get shortlisted applications
        shortlisted = Application.objects.filter(status='shortlisted')
        context['shortlisted'] = shortlisted

    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    """View user profile"""
    if request.user.role == 'candidate':
        skills = request.user.candidate_profile.skills.all()
        return render(request, 'profile.html', {'skills': skills})
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if request.user.role == 'candidate':
            profile_form = CandidateUpdateForm(request.POST, request.FILES, instance=request.user.candidate_profile)
        elif request.user.role == 'recruiter':
            profile_form = RecruiterUpdateForm(request.POST, instance=request.user.recruiter_profile)
        elif request.user.role == 'manager':
            profile_form = ManagerUpdateForm(request.POST, instance=request.user.manager_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

        if request.user.role == 'candidate':
            profile_form = CandidateUpdateForm(instance=request.user.candidate_profile)
        elif request.user.role == 'recruiter':
            profile_form = RecruiterUpdateForm(instance=request.user.recruiter_profile)
        elif request.user.role == 'manager':
            profile_form = ManagerUpdateForm(instance=request.user.manager_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'edit_profile.html', context)


# Job Views
@login_required
def job_list(request):
    """List all active jobs"""
    jobs = Job.objects.filter(status='active')
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    """View details of a specific job"""
    job = get_object_or_404(Job, id=job_id)

    # Check if candidate has already applied
    has_applied = False
    if request.user.role == 'candidate':
        has_applied = Application.objects.filter(
            candidate=request.user.candidate_profile,
            job=job
        ).exists()

    return render(request, 'job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })


@login_required
def job_create(request):
    """Create a new job posting"""
    if request.user.role != 'recruiter':
        return HttpResponseForbidden("You don't have permission to create jobs")

    if request.method == 'POST':
        form = JobForm(request.POST)
        formset = JobSkillFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.status = 'pending_approval'
            job.save()

            for skill_form in formset:
                if skill_form.cleaned_data and not skill_form.cleaned_data.get('DELETE', False):
                    skill = skill_form.save(commit=False)
                    skill.job = job
                    skill.save()

            messages.success(request, 'Job posting created and sent for approval!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm()
        formset = JobSkillFormSet(queryset=JobSkill.objects.none())

    return render(request, 'job_form.html', {'form': form, 'formset': formset})


@login_required
def job_edit(request, job_id):
    """Edit an existing job posting"""
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'recruiter' or job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this job")

    if job.status not in ['draft', 'pending_approval']:
        messages.error(request, 'Cannot edit a job that has been approved or is active.')
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        formset = JobSkillFormSet(request.POST, queryset=job.required_skills.all())

        if form.is_valid() and formset.is_valid():
            job = form.save()

            for skill_form in formset:
                if skill_form.cleaned_data:
                    if skill_form.cleaned_data.get('DELETE', False):
                        if skill_form.instance.pk:
                            skill_form.instance.delete()
                    else:
                        skill = skill_form.save(commit=False)
                        skill.job = job
                        skill.save()

            messages.success(request, 'Job posting updated successfully!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
        formset = JobSkillFormSet(queryset=job.required_skills.all())

    return render(request, 'job_form.html', {'form': form, 'formset': formset, 'job': job})


@login_required
def job_delete(request, job_id):
    """Delete a job posting"""
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'recruiter' or job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this job")

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job posting deleted successfully!')
        return redirect('manage_jobs')

    return render(request, 'job_confirm_delete.html', {'job': job})


@login_required
def manage_jobs(request):
    """Manage job postings for recruiters and managers"""
    if request.user.role == 'recruiter':
        jobs = Job.objects.filter(recruiter=request.user.recruiter_profile)
    elif request.user.role == 'manager':
        jobs = Job.objects.filter(status='pending_approval')
    else:
        return HttpResponseForbidden("You don't have permission to manage jobs")

    return render(request, 'manage_jobs.html', {'jobs': jobs})


@login_required
def approve_job(request, job_id):
    """Approve a pending job posting"""
    if request.user.role != 'manager':
        return HttpResponseForbidden("You don't have permission to approve jobs")

    job = get_object_or_404(Job, id=job_id)

    if job.status != 'pending_approval':
        messages.error(request, 'This job is not pending approval.')
        return redirect('manage_jobs')

    if request.method == 'POST':
        job.status = 'active'
        job.approved_by = request.user.manager_profile
        job.save()
        messages.success(request, 'Job approved successfully!')
        return redirect('manage_jobs')

    return render(request, 'approve_job.html', {'job': job})


# Application Views
@login_required
def application_list(request):
    """List applications for a candidate"""
    if request.user.role == 'candidate':
        applications = Application.objects.filter(candidate=request.user.candidate_profile)
    else:
        return HttpResponseForbidden("Only candidates can view their applications")

    return render(request, 'application_list.html', {'applications': applications})


@login_required
def application_create(request, job_id):
    """Create a new job application"""
    if request.user.role != 'candidate':
        return HttpResponseForbidden("Only candidates can apply for jobs")

    job = get_object_or_404(Job, id=job_id)

    # Check if already applied
    if Application.objects.filter(candidate=request.user.candidate_profile, job=job).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = request.user.candidate_profile
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('application_detail', application_id=application.id)
    else:
        form = ApplicationForm()

    return render(request, 'application_form.html', {'form': form, 'job': job})


@login_required
def application_detail(request, application_id):
    """View details of a specific application"""
    application = get_object_or_404(Application, id=application_id)

    # Permission check
    if request.user.role == 'candidate' and application.candidate.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this application")

    if request.user.role == 'recruiter' and application.job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this application")

    return render(request, 'application_detail.html', {'application': application})


@login_required
def withdraw_application(request, application_id):
    """Withdraw a job application"""
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'candidate' or application.candidate.user != request.user:
        return HttpResponseForbidden("You don't have permission to withdraw this application")

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Application withdrawn successfully!')
        return redirect('application_list')

    return render(request, 'withdraw_application.html', {'application': application})


@login_required
def manage_applications(request):
    """Manage applications for recruiters"""
    if request.user.role != 'recruiter':
        return HttpResponseForbidden("Only recruiters can manage applications")

    # Get all jobs posted by this recruiter
    recruiter_jobs = request.user.recruiter_profile.posted_jobs.all()

    # Get all applications for these jobs
    applications = Application.objects.filter(job__in=recruiter_jobs)

    return render(request, 'manage_applications.html', {'applications': applications})


@login_required
def review_application(request, application_id):
    """Review a job application"""
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'recruiter' or application.job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to review this application")

    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.reviewed_by = request.user.recruiter_profile
            application.save()
            messages.success(request, 'Application reviewed successfully!')
            return redirect('manage_applications')
    else:
        form = ApplicationReviewForm(instance=application)

    return render(request, 'review_application.html', {'form': form, 'application': application})


@login_required
def shortlist_application(request, application_id):
    """Shortlist a candidate's application"""
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'recruiter' or application.job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to shortlist this application")

    if request.method == 'POST':
        application.status = 'shortlisted'
        application.save()
        messages.success(request, 'Candidate shortlisted successfully!')
        return redirect('manage_applications')

    return render(request, 'shortlist_application.html', {'application': application})


@login_required
def schedule_interview(request, application_id):
    """Schedule an interview for a candidate"""
    application = get_object_or_404(Application, id=application_id)

    if request.user.role not in ['recruiter', 'manager']:
        return HttpResponseForbidden("You don't have permission to schedule interviews")

    if request.user.role == 'recruiter' and application.job.recruiter.user != request.user:
        return HttpResponseForbidden("You don't have permission to schedule interviews for this application")

    if application.status not in ['shortlisted', 'interview_scheduled']:
        messages.error(request, 'Can only schedule interviews for shortlisted candidates.')
        return redirect('application_detail', application_id=application.id)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application

            if request.user.role == 'manager':
                interview.assigned_by = request.user.manager_profile

            interview.save()

            # Update application status
            application.status = 'interview_scheduled'
            application.save()

            messages.success(request, 'Interview scheduled successfully!')
            return redirect('application_detail', application_id=application.id)
    else:
        form = InterviewForm()

    return render(request, 'schedule_interview.html', {'form': form, 'application': application})


@login_required
def interview_list(request):
    """List interviews for users based on their role"""
    if request.user.role == 'candidate':
        # Get all applications for this candidate
        applications = Application.objects.filter(candidate=request.user.candidate_profile)
        # Get all interviews for these applications
        interviews = Interview.objects.filter(application__in=applications)
    elif request.user.role in ['recruiter', 'manager']:
        # Get all interviews where this user is the interviewer
        interviews = Interview.objects.filter(interviewer=request.user)
    else:
        return HttpResponseForbidden("You don't have permission to view interviews")

    return render(request, 'interview_list.html', {'interviews': interviews})


# Skill Views
@login_required
def skill_list(request):
    """List all available skills"""
    skills = Skill.objects.all()
    return render(request, 'skill_list.html', {'skills': skills})


@login_required
def add_skill(request):
    """Add a new skill to the system"""
    if request.user.role != 'recruiter':
        return HttpResponseForbidden("Only recruiters can add skills to the system")

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('skill_list')
    else:
        form = SkillForm()

    return render(request, 'add_skill.html', {'form': form})


@login_required
def my_skills(request):
    """View and manage candidate skills"""
    if request.user.role != 'candidate':
        return HttpResponseForbidden("Only candidates can view their skills")

    candidate_skills = CandidateSkill.objects.filter(candidate=request.user.candidate_profile)

    if request.method == 'POST':
        form = CandidateSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.candidate = request.user.candidate_profile

            # Check if skill already exists for this candidate
            if CandidateSkill.objects.filter(candidate=request.user.candidate_profile, skill=skill.skill).exists():
                messages.error(request, 'You already have this skill in your profile.')
            else:
                skill.save()
                messages.success(request, 'Skill added to your profile!')

            return redirect('my_skills')
    else:
        form = CandidateSkillForm()

    # Exclude skills already added by the candidate
    existing_skills = candidate_skills.values_list('skill', flat=True)
    form.fields['skill'].queryset = Skill.objects.exclude(id__in=existing_skills)

    return render(request, 'my_skills.html', {
        'candidate_skills': candidate_skills,
        'form': form
    })


@login_required
def add_skill_to_profile(request, skill_id):
    """Add existing skill to candidate profile"""
    if request.user.role != 'candidate':
        return HttpResponseForbidden("Only candidates can add skills to their profile")

    skill = get_object_or_404(Skill, id=skill_id)

    # Check if already exists
    if CandidateSkill.objects.filter(candidate=request.user.candidate_profile, skill=skill).exists():
        messages.error(request, 'You already have this skill in your profile.')
        return redirect('my_skills')

    if request.method == 'POST':
        form = CandidateSkillForm(request.POST)
        if form.is_valid():
            candidate_skill = form.save(commit=False)
            candidate_skill.candidate = request.user.candidate_profile
            candidate_skill.skill = skill
            candidate_skill.save()
            messages.success(request, f'{skill.name} added to your profile!')
            return redirect('my_skills')
    else:
        form = CandidateSkillForm(initial={'skill': skill})
        form.fields['skill'].widget.attrs['disabled'] = True

    return render(request, 'add_skill_to_profile.html', {'form': form, 'skill': skill})


@login_required
def remove_skill_from_profile(request, skill_id):
    """Remove skill from candidate profile"""
    if request.user.role != 'candidate':
        return HttpResponseForbidden("Only candidates can remove skills from their profile")

    candidate_skill = get_object_or_404(
        CandidateSkill,
        candidate=request.user.candidate_profile,
        skill_id=skill_id
    )

    if request.method == 'POST':
        candidate_skill.delete()
        messages.success(request, 'Skill removed from your profile!')
        return redirect('my_skills')

    return render(request, 'remove_skill_from_profile.html', {'candidate_skill': candidate_skill})


# Filter candidates by skills
@login_required
def filter_candidates_by_skills(request):
    """Filter candidates based on skills"""
    if request.user.role != 'recruiter':
        return HttpResponseForbidden("Only recruiters can filter candidates by skills")

    candidates = Candidate.objects.all()
    skills = Skill.objects.all()

    if request.method == 'GET':
        selected_skills = request.GET.getlist('skills')
        min_proficiency = request.GET.get('min_proficiency')

        if selected_skills:
            # Filter candidates who have all the selected skills
            for skill_id in selected_skills:
                candidates = candidates.filter(skills__skill_id=skill_id)

            if min_proficiency:
                # Further filter by minimum proficiency level
                candidates = candidates.filter(skills__proficiency_level__gte=min_proficiency)

    return render(request, 'filter_candidates.html', {
        'candidates': candidates,
        'skills': skills
    })


# Final hiring decision
@login_required
def finalize_hiring(request, application_id):
    """Make final hiring decision on a candidate"""
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'manager':
        return HttpResponseForbidden("Only managers can make final hiring decisions")

    if application.status not in ['interview_scheduled', 'offered']:
        messages.error(request, 'Can only make hiring decisions for interviewed candidates.')
        return redirect('application_detail', application_id=application.id)

    if request.method == 'POST':
        decision = request.POST.get('decision')

        if decision == 'hire':
            application.status = 'hired'
            messages.success(request, f'{application.candidate.user.get_full_name()} has been hired!')
        elif decision == 'reject':
            application.status = 'rejected'
            messages.success(request, 'Application has been rejected.')
        elif decision == 'offer':
            application.status = 'offered'
            messages.success(request, 'Job offer has been sent to the candidate.')

        application.save()
        return redirect('application_detail', application_id=application.id)

    return render(request, 'finalize_hiring.html', {'application': application})