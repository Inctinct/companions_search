from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pet_project.models import Project
from apps.pet_project.project_list.services import ProjectListPagination
from apps.pet_project.serializers import PetProjectGetSerializer


# Create your views here.


class ProjectListView(APIView, ProjectListPagination):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Project.objects.prefetch_related("projecttag_set").all()
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = PetProjectGetSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)
