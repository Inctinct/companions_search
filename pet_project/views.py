from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from pet_project.serializers import PetProjectSerializer, PetProjectGetSerializer
from pet_project.models import Tags, ProjectTag, Project
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class PetProjectView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=PetProjectGetSerializer,
        request_method="GET",
        responses={200: PetProjectGetSerializer},
    )
    def get(self, request):
        project = Project.objects.prefetch_related("projecttag_set").get(
            id=request.GET.get("project_id"), user_id=request.user
        )
        data = model_to_dict(project)
        data["tags"] = [model_to_dict(tag) for tag in project.projecttag_set.all()]
        serializer = PetProjectGetSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=201)

    @swagger_auto_schema(
        request_body=PetProjectSerializer,
        request_method="POST",
        responses={200: PetProjectSerializer},
    )
    def post(self, request):
        data = request.data
        serializer = PetProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        tags = data.pop("tags")

        project, created = Project.objects.get_or_create(user_id=request.user, **data)
        try:
            if created is True:
                tags = ProjectTag.objects.bulk_create(
                    [
                        ProjectTag(
                            project_id=project,
                            union_type=tag.pop("union_type"),
                            tag_id=Tags.objects.get_or_create(**tag)[0],
                        )
                        for tag in tags
                    ]
                )
            project.save()
        except Exception as e:
            project.delete()
            return Response(status=404)

        return Response(project.id, status=201)

    @swagger_auto_schema(
        request_body=PetProjectSerializer,
        request_method="PUT",
        responses={200: PetProjectSerializer},
    )
    def put(self, request):
        data = request.data
        project = Project.objects.get(
            id=request.GET.get("project_id"), user_id=request.user
        )
        serializer = PetProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        tags = data.pop("tags")

        Project.objects.filter(
            id=request.GET.get("project_id"), user_id=request.user
        ).update(**data)
        ProjectTag.objects.filter(project_id=project).delete()
        ProjectTag.objects.bulk_create(
            [
                ProjectTag(
                    project_id=project,
                    union_type=tag.pop("union_type"),
                    tag_id=Tags.objects.get_or_create(**tag)[0],
                )
                for tag in tags
            ]
        )
        project.save()
        return Response(project.id, status=201)

    def delete(self, request):
        try:
            project = Project.objects.get(
                id=request.GET.get("project_id"), user_id=request.user
            ).delete()
        except Exception:
            return Response(status=404)

        return Response(status=201)
