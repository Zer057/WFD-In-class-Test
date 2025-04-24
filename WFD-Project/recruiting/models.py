from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='candidates')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Job(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_jobs')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_jobs')
    required_skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewing', 'Interviewing'),
        ('offered', 'Offer Extended'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    notes = models.TextField(blank=True)
    interviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_interviews')

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate} - {self.job}"