from django.contrib import admin
from .models import RetailRole, UserProfile, Skill, Candidate, CandidateSkill, Position, Application

@admin.register(RetailRole)
class RetailRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'importance')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ('skills',)

@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'skill', 'proficiency')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'is_open', 'created_at')
    list_filter = ('department', 'is_open')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'status', 'application_date')
    list_filter = ('status',)