# models.py
from django.db import models
from .managers import OrderedManager
from django.conf import settings
import os


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
        return f"File {self.id}"


class Task(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=50,
        choices=[("running", "Running"), ("error", "Error"), ("success", "Success")],
    )
    message = models.TextField()
    biz_type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="task_files/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_file = models.ForeignKey(
        CaibaoFile,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    
    def save(self, *args, **kwargs):
        upload_file_folder = self.source_file.file_path.split(os.sep)[-2]
        self.file.upload_to = os.path.join("task_files", upload_file_folder)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"
