from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.pet_project.models import Tags, ProjectTag, Project


class ProjectTagSerializer(ModelSerializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False)
    union_type = serializers.CharField()

    class Meta:
        model = Tags
        fields = ["id", "name", "union_type"]


class PetProjectSerializer(ModelSerializer):
    tags = ProjectTagSerializer(many=True)

    class Meta:
        model = Project
        fields = ["title", "description", "repository", "tags"]


class ProjectTagGetSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, data):
        return data.tag_id.name

    class Meta:
        model = ProjectTag
        fields = ["union_type", "tag_id", "name"]


class PetProjectGetSerializer(ModelSerializer):
    projecttag_set = ProjectTagGetSerializer(many=True)

    class Meta:
        model = Project
        fields = ["id", "title", "description", "repository", "projecttag_set"]
