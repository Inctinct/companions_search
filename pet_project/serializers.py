from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from pet_project.models import Tags, ProjectTag, Project


class ProjectTagSerializer(ModelSerializer):
    tag = serializers.CharField()

    class Meta:
        model = ProjectTag
        fields = ["tag", "tag_type"]


class PetProjectSerializer(ModelSerializer):
    tags = ProjectTagSerializer(many=True)

    class Meta:
        model = Project
        fields = ["title", "description", "repository", "tags"]
