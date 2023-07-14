from django.contrib import admin
from .models import Project, ProjectTag, Tags

# Register your models here.


admin.site.register(Project),
admin.site.register(ProjectTag),
admin.site.register(Tags)
