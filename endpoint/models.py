from django.db import models
from .managers import OrderedManager
from django.conf import settings
import os, logging

logger = logging.getLogger(__name__)

class TaskStatus(models.TextChoices):
    RUNNING = 'running', 'Running'
    ERROR = 'error', 'Error'
    SUCCESS = 'success', 'Success'


class OCREndpoint(models.Model):
    url = models.URLField(max_length=1024, null=False, blank=False)
    capacity = models.IntegerField(default=3)
    current_load = models.IntegerField(default=0)

    def __str__(self):
        return f'OCREndpoint cap {self.capacity} - load {self.current_load} - {self.url}'
    
class Company(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderedManager()

    def __str__(self):
        return f"{self.name} - {self.code}"


class CaibaoFile(models.Model):
    file_path = models.CharField(max_length=2048)
    hash_digest = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="caibao_files"
    )
    priority = models.IntegerField(default=0)

    objects = OrderedManager()

    def __str__(self):
        return f"File {self.id} - {self.file_path}"


def _dynamic_upload_to(task_obj, file):
    upload_sub_paths = task_obj.source_file.file_path.split(os.sep)[-2:]
    upload_to_path = os.path.join("task_files", *upload_sub_paths)
    dot_index = upload_to_path.rfind('.')
    if dot_index > -1:
        upload_to_path = f"{upload_to_path[:dot_index]}.{settings.OCR_OUTPUT_FORMAT}"
    else:
        upload_to_path = f"{upload_to_path}.{settings.OCR_OUTPUT_FORMAT}"
    logger.debug(f'upload_to_path: {upload_to_path}')
    return upload_to_path

class Task(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=50,
        choices=TaskStatus.choices,
    )
    message = models.TextField()
    biz_type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=_dynamic_upload_to, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_file = models.ForeignKey(
        CaibaoFile,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    
    endpoint = models.ForeignKey(
        OCREndpoint, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    
    def __str__(self):
        return f"Task {self.task_id} - {self.status}"
    

