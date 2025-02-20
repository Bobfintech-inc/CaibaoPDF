# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskStatusUpdateSerializer


class TaskStatusUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize the incoming data
        serializer = TaskStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if it's a success callback with a file
            task_data = serializer.validated_data
            task_id = task_data["task_id"]
            task, created = Task.objects.update_or_create(
                task_id=task_id, defaults=task_data
            )

            if task_data["status"] == "success" and "file" in request.FILES:
                # Save the file when the task status is 'success'
                task.file = request.FILES["file"]
                task.save()

            task_data.pop("file", None)
            return Response(
                {"message": "Task status updated successfully!", "data": task_data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
