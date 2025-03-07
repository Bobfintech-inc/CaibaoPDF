# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Task, TaskStatus
from .serializers import TaskStatusUpdateSerializer
import logging

logger = logging.getLogger(__name__)

class TaskStatusUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize the incoming data
        serializer = TaskStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if it's a success callback with a file
            task_data = serializer.validated_data
            logger.info(f"validated_data + {serializer.validated_data}")
            task_id = task_data["task_id"]
            
            with transaction.atomic():
                task = Task.objects.get(task_id=task_id)
                logger.debug(f'Updating task {task}')
                task.status = task_data["status"]
                task.message = task_data["message"]
                if task_data['status'] in [TaskStatus.ERROR.value, TaskStatus.SUCCESS.value]:
                    task.endpoint.current_load -= 1
                    task.endpoint.save()
                    
                task.save()
                try:
                    
                    if task_data["status"] == "success" and "file" in request.FILES:
                        # Save the file when the task status is 'success'
                        task.file = request.FILES["file"]
                        task.save()
                        
                except Exception as e:
                    logger.exception(e)
                    task.file = None
                    task.status = TaskStatus.ERROR.value
                    task.message = str(e)
                    task.save()
                    raise e


            task_data.pop("file", None)
            return Response(
                {"message": "Task status updated successfully!", "data": task_data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
