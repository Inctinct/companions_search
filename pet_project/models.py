from django.contrib.auth.models import User
from django.db import models

from pet_project.validators import validate_github_url


class Tags(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


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
    TAG_TYPE = (("In search", "In search"), ("I use", "I use"))
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_type = models.CharField(max_length=10, choices=TAG_TYPE)
