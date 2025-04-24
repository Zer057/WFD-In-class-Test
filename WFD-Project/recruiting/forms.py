from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate, Skill, Job, Application


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['phone', 'address', 'resume']


class SkillSelectionForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'department', 'location', 'closing_date', 'required_skills']
        widgets = {
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
            'required_skills': forms.CheckboxSelectMultiple(),
        }


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'notes']


class InterviewerAssignmentForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['interviewer']