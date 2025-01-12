import uuid
from django.db import models

# Create your models here.
class ProjectType(models.Model):
    project_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_info = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'project_type'
        verbose_name_plural = 'Project Type'
        
    def __str__(self):
        return self.project_type
    
class ImageMode(models.Model):
    mode = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'image_mode'
        verbose_name_plural = 'Image Mode'
        
    def __str__(self):
        return self.mode

class Project(models.Model):
    project_id = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    annotation_group = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_info = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'project'
        verbose_name_plural = 'Project'
        
    def __str__(self):
        return f'{self.project_name} - {self.project_type}'
    
    
class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image_id = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')
    annotated = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    mode = models.ForeignKey(ImageMode, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'image'
        verbose_name_plural = 'Images'
        
    def __str__(self):
        return self.image_name
    
    