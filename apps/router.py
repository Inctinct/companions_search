from django.urls import path, include


urlpatterns = [
    path("", include("apps.user.urls")),
    path("", include("apps.pet_project.urls")),
    path("", include("apps.pet_project.project_list.urls")),
]
