from django.urls import path, include


urlpatterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.pet_project.urls")),
    path("", include("apps.pet_project.project_list.urls")),
]
