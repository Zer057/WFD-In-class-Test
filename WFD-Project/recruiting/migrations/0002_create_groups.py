from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups(apps, schema_editor):
    # Create groups
    candidate_group, _ = Group.objects.get_or_create(name='Candidate')
    recruiter_group, _ = Group.objects.get_or_create(name='Recruiter')
    manager_group, _ = Group.objects.get_or_create(name='Manager')

class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]