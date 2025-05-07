from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    """Represents a candidate linked to an authenticated user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # link to auth user
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    """Represents a skill that can be linked to candidates and required by jobs."""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CandidateSkill(models.Model):
    """Maps a candidate to a skill with a proficiency level."""
    PROFICIENCY_LEVELS = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced')
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.IntegerField(choices=PROFICIENCY_LEVELS)

    def __str__(self):
        return f"{self.candidate.user.username} - {self.skill.name} ({self.get_proficiency_display()})"

class Job(models.Model):
    """Represents a job listing with required skills."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, related_name='jobs')

    def __str__(self):
        return self.title

class Application(models.Model):
    """Represents a candidate's application to a job."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.candidate.user.username} applied for {self.job.title} ({self.status})"
