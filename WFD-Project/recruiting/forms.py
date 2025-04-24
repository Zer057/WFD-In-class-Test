# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import (
    User, Candidate, Recruiter, Manager, Job, JobSkill,
    Application, Interview, Skill, CandidateSkill
)


# User and Profile Forms
class UserRegisterForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField()
    role = forms.ChoiceField(
        choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter'), ('manager', 'Manager')],
        initial='candidate'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CandidateUpdateForm(forms.ModelForm):
    """Form for updating candidate profile"""

    class Meta:
        model = Candidate
        fields = ['phone', 'resume', 'experience_years']
        widgets = {
            'resume': forms.FileInput()
        }


class RecruiterUpdateForm(forms.ModelForm):
    """Form for updating recruiter profile"""

    class Meta:
        model = Recruiter
        fields = ['department']


class ManagerUpdateForm(forms.ModelForm):
    """Form for updating manager profile"""

    class Meta:
        model = Manager
        fields = ['department']


# Job Forms
class JobForm(forms.ModelForm):
    """Form for creating/editing jobs"""

    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'salary_range', 'closing_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'closing_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class JobSkillForm(forms.ModelForm):
    """Form for job required skills"""

    class Meta:
        model = JobSkill
        fields = ['skill', 'importance']
        widgets = {
            'importance': forms.Select(
                choices=[(i,
                          f"{i} - {'Very Important' if i == 5 else 'Important' if i == 4 else 'Neutral' if i == 3 else 'Less Important' if i == 2 else 'Optional'}")
                         for i in range(1, 6)]
            )
        }


# Create formset for managing multiple skills per job
JobSkillFormSet = inlineformset_factory(
    Job, JobSkill, form=JobSkillForm,
    extra=3, can_delete=True
)


# Application Forms
class ApplicationForm(forms.ModelForm):
    """Form for job applications"""

    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5})
        }


class ApplicationReviewForm(forms.ModelForm):
    """Form for reviewing applications"""

    class Meta:
        model = Application
        fields = ['status', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4})
        }


# Interview Forms
class InterviewForm(forms.ModelForm):
    """Form for scheduling interviews"""

    class Meta:
        model = Interview
        fields = ['interviewer', 'scheduled_date', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        # Only managers and recruiters can be interviewers
        self.fields['interviewer'].queryset = User.objects.filter(role__in=['manager', 'recruiter'])


class InterviewFeedbackForm(forms.ModelForm):
    """Form for providing interview feedback"""

    class Meta:
        model = Interview
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 5})
        }


# Skill Forms
class SkillForm(forms.ModelForm):
    """Form for creating skills"""

    class Meta:
        model = Skill
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class CandidateSkillForm(forms.ModelForm):
    """Form for adding skills to candidate profile"""

    class Meta:
        model = CandidateSkill
        fields = ['skill', 'proficiency_level', 'years_experience']
        widgets = {
            'proficiency_level': forms.Select(
                choices=[(i,
                          f"{i} - {'Expert' if i == 5 else 'Advanced' if i == 4 else 'Intermediate' if i == 3 else 'Basic' if i == 2 else 'Beginner'}")
                         for i in range(1, 6)]
            )
        }


# Candidate Search Form
class CandidateSearchForm(forms.Form):
    """Form for searching candidates by skills"""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    min_proficiency = forms.ChoiceField(
        choices=[(i,
                  f"{i} - {'Expert' if i == 5 else 'Advanced' if i == 4 else 'Intermediate' if i == 3 else 'Basic' if i == 2 else 'Beginner'}")
                 for i in range(1, 6)],
        required=False
    )
    min_experience = forms.IntegerField(
        required=False,
        min_value=0
    )


# Date Range Filter Form
class DateRangeFilterForm(forms.Form):
    """Form for filtering by date range"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )