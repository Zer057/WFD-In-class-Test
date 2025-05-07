from django.test import TestCase
from django.contrib.auth.models import User
from .models import Candidate, Skill, CandidateSkill, Job, Application

class CandidateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='pass123')
        self.candidate = Candidate.objects.create(user=self.user)

    def test_candidate_str(self):
        self.assertEqual(str(self.candidate), 'johndoe')

class SkillModelTest(TestCase):
    def test_skill_str(self):
        skill = Skill.objects.create(name='Python', description='Programming Language')
        self.assertEqual(str(skill), 'Python')

class CandidateSkillModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='janedoe', password='pass123')
        self.candidate = Candidate.objects.create(user=self.user)
        self.skill = Skill.objects.create(name='Django')

    def test_candidate_skill_str(self):
        candidate_skill = CandidateSkill.objects.create(candidate=self.candidate, skill=self.skill, proficiency=2)
        self.assertEqual(
            str(candidate_skill),
            'janedoe - Django (Intermediate)'
        )

class JobModelTest(TestCase):
    def test_job_str(self):
        job = Job.objects.create(title='Backend Developer', description='Build APIs')
        self.assertEqual(str(job), 'Backend Developer')

    def test_job_skills_required(self):
        job = Job.objects.create(title='Frontend Developer', description='Build UIs')
        skill1 = Skill.objects.create(name='HTML')
        skill2 = Skill.objects.create(name='CSS')
        job.skills_required.set([skill1, skill2])
        self.assertEqual(job.skills_required.count(), 2)

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='markdoe', password='pass123')
        self.candidate = Candidate.objects.create(user=self.user)
        self.skill = Skill.objects.create(name='React')
        self.job = Job.objects.create(title='Fullstack Developer', description='Work on frontend and backend')
        self.job.skills_required.add(self.skill)

    def test_application_str(self):
        app = Application.objects.create(candidate=self.candidate, job=self.job)
        self.assertEqual(
            str(app),
            f"markdoe applied for Fullstack Developer (Pending)"
        )

    def test_application_default_status(self):
        app = Application.objects.create(candidate=self.candidate, job=self.job)
        self.assertEqual(app.status, 'Pending')
