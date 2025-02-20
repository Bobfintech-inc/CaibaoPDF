# serializers.py
from rest_framework import serializers
from .models import Task


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    taskId = serializers.CharField(source="task_id")  # Maps taskId to task_id
    bizType = serializers.CharField(source="biz_type", required=False)  # Maps bizType to biz_type
    fileName = serializers.CharField(
        source="file_name", required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = ["taskId", "status", "message", "bizType", "fileName", "file"]
        extra_kwargs = {"file": {"required": False}, "bizType": {"required": False}}
