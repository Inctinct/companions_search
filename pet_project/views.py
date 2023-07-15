from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from pet_project.serializers import PetProjectSerializer
from pet_project.models import Tags, ProjectTag, Project
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class PetProjectView(APIView):
    permission_classes = (IsAuthenticated,)

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

        project, created = Project.objects.get_or_create(user=request.user, **data)
        try:
            if created is True:
                tags = ProjectTag.objects.bulk_create(
                    [
                        ProjectTag(
                            project=project,
                            union_type=tag.pop('union_type'),
                            tag_name=Tags.objects.get_or_create(**tag)[0],
                        )
                        for tag in tags
                    ]
                )
            project.save()
        except Exception as e:
            project.delete()
            return Response(status=404)

        return Response(serializer.data, status=200)
