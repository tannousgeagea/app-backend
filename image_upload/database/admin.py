from django.contrib import admin
from .models import ProjectType, ImageMode, Project, Image

@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('project_type', 'description', 'created_at')
    search_fields = ('project_type', 'description')
    list_filter = ('created_at',)

@admin.register(ImageMode)
class ImageModeAdmin(admin.ModelAdmin):
    list_display = ('mode', 'description', 'created_at')
    search_fields = ('mode', 'description')
    list_filter = ('created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_type', 'annotation_group', 'description', 'created_at')
    search_fields = ('project_name', 'annotation_group', 'description', 'project_type__project_type')
    list_filter = ('created_at', 'project_type')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'project', 'image_file', 'annotated', 'processed', 'mode')
    search_fields = ('image_name', 'project__project_name', 'project__project_type__project_type', 'mode__mode')
    list_filter = ('annotated', 'processed', 'mode', 'project')
