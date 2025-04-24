from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Count, Q
from .models import Candidate, Skill, Job, Application
from .forms import (
    UserRegisterForm, CandidateProfileForm, SkillSelectionForm,
    JobForm, ApplicationReviewForm, InterviewerAssignmentForm
)


# Helper functions to check user roles
def is_candidate(user):
    return user.groups.filter(name='Candidate').exists()


def is_recruiter(user):
    return user.groups.filter(name='Recruiter').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


# Home/Dashboard view
@login_required
def home(request):
    if is_candidate(request.user):
        # For candidates, show available jobs and application status
        try:
            candidate = request.user.candidate
            applications = candidate.applications.all()
            jobs = Job.objects.filter(status='approved')
            return render(request, 'recruitment/candidate_dashboard.html', {
                'applications': applications,
                'jobs': jobs[:5]  # Show 5 latest jobs
            })
        except Candidate.DoesNotExist:
            messages.warning(request, "Please complete your profile")
            return redirect('recruitment:edit_profile')

    elif is_recruiter(request.user):
        # For recruiters, show jobs they created and recent applications
        jobs = Job.objects.filter(created_by=request.user)
        recent_applications = Application.objects.filter(job__created_by=request.user).order_by('-applied_date')[:10]
        return render(request, 'recruitment/recruiter_dashboard.html', {
            'jobs': jobs,
            'recent_applications': recent_applications
        })

    elif is_manager(request.user):
        # For managers, show pending approvals and hiring statistics
        pending_jobs = Job.objects.filter(status='pending')
        shortlisted = Application.objects.filter(status='shortlisted').count()
        interviewing = Application.objects.filter(status='interviewing').count()
        hiring_stats = {
            'shortlisted': shortlisted,
            'interviewing': interviewing,
            'offered': Application.objects.filter(status='offered').count(),
            'hired': Application.objects.filter(status='hired').count(),
        }
        return render(request, 'recruitment/manager_dashboard.html', {
            'pending_jobs': pending_jobs,
            'hiring_stats': hiring_stats
        })

    # If user doesn't belong to any specific group
    return render(request, 'recruitment/home.html')


# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to the Candidate group
            candidate_group = Group.objects.get(name='Candidate')
            candidate_group.user_set.add(user)
            # Create a Candidate profile
            Candidate.objects.create(user=user)
            messages.success(request, 'Account created! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'recruitment/register.html', {'form': form})


# Candidate views
@login_required
@user_passes_test(is_candidate)
def edit_profile(request):
    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        candidate = Candidate.objects.create(user=request.user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('recruitment:home')
    else:
        form = CandidateProfileForm(instance=candidate)

    return render(request, 'recruitment/edit_profile.html', {'form': form})


@login_required
@user_passes_test(is_candidate)
def add_skills(request):
    candidate = request.user.candidate

    if request.method == 'POST':
        form = SkillSelectionForm(request.POST)
        if form.is_valid():
            selected_skills = form.cleaned_data['skills']
            candidate.skills.set(selected_skills)
            messages.success(request, 'Your skills have been updated!')
            return redirect('recruitment:home')
    else:
        form = SkillSelectionForm(initial={'skills': candidate.skills.all()})

    return render(request, 'recruitment/add_skills.html', {'form': form})


@login_required
def job_list(request):
    jobs = Job.objects.filter(status='approved')
    return render(request, 'recruitment/job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the candidate has already applied
    already_applied = False
    if is_candidate(request.user):
        try:
            candidate = request.user.candidate
            already_applied = Application.objects.filter(candidate=candidate, job=job).exists()
        except Candidate.DoesNotExist:
            pass

    return render(request, 'recruitment/job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })


@login_required
@user_passes_test(is_candidate)
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='approved')
    candidate = request.user.candidate

    # Check if already applied
    if Application.objects.filter(candidate=candidate, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('recruitment:job_detail', job_id=job.id)

    # Create application
    Application.objects.create(candidate=candidate, job=job)
    messages.success(request, f'You have successfully applied for {job.title}!')
    return redirect('recruitment:my_applications')


@login_required
@user_passes_test(is_candidate)
def my_applications(request):
    try:
        candidate = request.user.candidate
        applications = candidate.applications.all().order_by('-applied_date')
    except Candidate.DoesNotExist:
        applications = []
        messages.warning(request, "Please complete your profile first.")
        return redirect('recruitment:edit_profile')

    return render(request, 'recruitment/my_applications.html', {'applications': applications})


# Recruiter views
@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            # If created by manager, automatically approve
            if is_manager(request.user):
                job.status = 'approved'
                job.approved_by = request.user
            else:
                job.status = 'pending'
            job.save()
            form.save_m2m()  # Save many-to-many fields (required_skills)
            messages.success(request, 'Job posting created!')
            return redirect('recruitment:home')
    else:
        form = JobForm()

    return render(request, 'recruitment/create_job.html', {'form': form})


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only creator or manager can edit
    if not (job.created_by == request.user or is_manager(request.user)):
        messages.error(request, "You don't have permission to edit this job.")
        return redirect('recruitment:home')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            # If edited by recruiter, set back to pending
            if is_recruiter(request.user) and not is_manager(request.user):
                job = form.save(commit=False)
                job.status = 'pending'
                job.approved_by = None
                job.save()
                form.save_m2m()
            else:
                form.save()
            messages.success(request, 'Job posting updated!')
            return redirect('recruitment:job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)

    return render(request, 'recruitment/edit_job.html', {'form': form, 'job': job})


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only creator or manager can view applicants
    if not (job.created_by == request.user or is_manager(request.user)):
        messages.error(request, "You don't have permission to view applicants for this job.")
        return redirect('recruitment:home')

    applications = job.applications.all().select_related('candidate__user')

    # Filter by status if requested
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'recruitment/job_applicants.html', {
        'job': job,
        'applications': applications,
        'status_filter': status_filter
    })


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def candidate_list(request):
    candidates = Candidate.objects.all().select_related('user')

    # Filter by skill if requested
    skills = Skill.objects.all()

    return render(request, 'recruitment/candidate_list.html', {
        'candidates': candidates,
        'skills': skills
    })


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def candidates_by_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    candidates = Candidate.objects.filter(skills=skill).select_related('user')

    return render(request, 'recruitment/candidates_by_skill.html', {
        'skill': skill,
        'candidates': candidates
    })


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def review_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Only job creator or manager can review
    if not (application.job.created_by == request.user or is_manager(request.user)):
        messages.error(request, "You don't have permission to review this application.")
        return redirect('recruitment:home')

    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated!')
            return redirect('recruitment:job_applicants', job_id=application.job.id)
    else:
        form = ApplicationReviewForm(instance=application)

    return render(request, 'recruitment/review_application.html', {
        'form': form,
        'application': application
    })


@login_required
@user_passes_test(lambda u: is_recruiter(u) or is_manager(u))
def shortlist_candidate(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Only job creator or manager can shortlist
    if not (application.job.created_by == request.user or is_manager(request.user)):
        messages.error(request, "You don't have permission to shortlist this candidate.")
        return redirect('recruitment:home')

    application.status = 'shortlisted'
    application.save()
    messages.success(request, f'{application.candidate.user.get_full_name()} has been shortlisted!')

    return redirect('recruitment:job_applicants', job_id=application.job.id)


# Manager views
@login_required
@user_passes_test(is_manager)
def pending_jobs(request):
    jobs = Job.objects.filter(status='pending')
    return render(request, 'recruitment/pending_jobs.html', {'jobs': jobs})


@login_required
@user_passes_test(is_manager)
def approve_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='pending')
    job.status = 'approved'
    job.approved_by = request.user
    job.save()
    messages.success(request, f'Job posting "{job.title}" has been approved!')
    return redirect('recruitment:pending_jobs')


@login_required
@user_passes_test(is_manager)
def shortlisted_candidates(request):
    applications = Application.objects.filter(
        Q(status='shortlisted') | Q(status='interviewing')
    ).select_related('candidate__user', 'job')

    return render(request, 'recruitment/shortlisted_candidates.html', {'applications': applications})


@login_required
@user_passes_test(is_manager)
def assign_interviewer(request, application_id):
    application = get_object_or_404(Application, id=application_id, status='shortlisted')

    if request.method == 'POST':
        form = InterviewerAssignmentForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = 'interviewing'
            application.save()
            messages.success(request, f'Interviewer assigned for {application.candidate.user.get_full_name()}!')
            return redirect('recruitment:shortlisted_candidates')
    else:
        form = InterviewerAssignmentForm(instance=application)

    return render(request, 'recruitment/assign_interviewer.html', {
        'form': form,
        'application': application
    })


@login_required
@user_passes_test(is_manager)
def finalize_hiring(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        decision = request.POST.get('decision')

        if decision == 'hire':
            application.status = 'hired'
            messages.success(request, f'{application.candidate.user.get_full_name()} has been hired!')
        elif decision == 'reject':
            application.status = 'rejected'
            messages.info(request, f'{application.candidate.user.get_full_name()} has been rejected.')
        elif decision == 'offer':
            application.status = 'offered'
            messages.success(request, f'Offer extended to {application.candidate.user.get_full_name()}!')

        application.save()
        return redirect('recruitment:shortlisted_candidates')

    return render(request, 'recruitment/finalize_hiring.html', {'application': application})