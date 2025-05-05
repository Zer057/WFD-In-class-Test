from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    candidates = models.ManyToManyField(User, related_name='skills')

    def __str__(self):
        return self.name
