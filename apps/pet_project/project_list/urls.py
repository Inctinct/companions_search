from django.urls import re_path

from apps.pet_project.project_list.views import ProjectListView

urlpatterns = [
    re_path(r"^projects/", ProjectListView.as_view(), name="project-list"),
]
