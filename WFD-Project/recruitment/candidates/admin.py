from django.contrib import admin
from .models import Candidate, Skill, CandidateSkill, Job, Application

admin.site.register(Candidate)
admin.site.register(Skill)
admin.site.register(CandidateSkill)
admin.site.register(Job)
admin.site.register(Application)
