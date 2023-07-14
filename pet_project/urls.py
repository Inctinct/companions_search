from django.urls import re_path

from pet_project.views import PetProjectView

urlpatterns = [
    re_path(r"^pet-project/", PetProjectView.as_view(), name="pet-project"),
]
