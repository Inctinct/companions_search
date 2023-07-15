import uuid

from django.contrib.auth.models import User
from django.db import models

from pet_project.validators import validate_github_url


class Tags(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    repository = models.URLField(
        validators=[validate_github_url], null=True, blank=True
    )

    def __str__(self):
        return self.title


class ProjectTag(models.Model):
    TYPE = (("In search", "In search"), ("I use", "I use"))
    tag_name = models.ForeignKey(Tags, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    union_type = models.CharField(max_length=10, choices=TYPE)
