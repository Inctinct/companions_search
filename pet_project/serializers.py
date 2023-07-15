from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from pet_project.models import Tags, ProjectTag, Project


class ProjectTagSerializer(ModelSerializer):
    uuid = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = ProjectTag
        fields = ["name", "union_type", "uuid"]


class PetProjectSerializer(ModelSerializer):
    tags = ProjectTagSerializer(many=True)

    class Meta:
        model = Project
        fields = ["title", "description", "repository", "tags"]

