# serializers.py
from rest_framework import serializers
from .models import Task, TaskStatus
import logging
logger = logging.getLogger(__name__)

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    taskId = serializers.CharField(source="task_id")  # Maps taskId to task_id
    bizType = serializers.CharField(source="biz_type", required=False)  # Maps bizType to biz_type
    fileName = serializers.CharField(
        source="file_name", required=False, allow_null=True
    )
    status = serializers.CharField()

    class Meta:
        model = Task
        fields = ["taskId", "status", "message", "bizType", "fileName", "file"]
        extra_kwargs = {"file": {"required": False}, "bizType": {"required": False}}

    def validate_status(self, value):
        logger.debug(f"Validating status: {value}")
        if value not in TaskStatus.values:
            raise serializers.ValidationError("Invalid status value")
        return value

    def to_internal_value(self, data):
        logger.debug(f"to_internal_value: {data}")
        data = super().to_internal_value(data)
        # Convert the status to TaskStatus enum
        data['status'] = TaskStatus(data['status'])
        return data