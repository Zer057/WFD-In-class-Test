from django import forms
from .models import Job, Skill, Candidate

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume']  # we exclude user here because it will be linked automatically
