from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from pet_project.serializers import PetProjectSerializer
from pet_project.models import Tags, ProjectTag, Project


# Create your views here.


class PetProjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = PetProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        tags = data.pop("tags")
        try:
            project, created = Project.objects.get_or_create(user=request.user, **data)
            if created is True:
                ProjectTag.objects.bulk_create(
                    [
                        ProjectTag(
                            project=project,
                            tag_type=tag["tag_type"],
                            tag=Tags.objects.get_or_create(tag=tag["tag"])[0],
                        )
                        for tag in tags
                    ]
                )
            project.save()
        except Exception as e:
            project.delete()
            return Response(status=404)

        return Response(serializer.data, status=200)
