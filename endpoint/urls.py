# urls.py
from django.urls import path
from .views import TaskStatusUpdateView

urlpatterns = [
    path("task/update/", TaskStatusUpdateView.as_view(), name="task-status-update"),
]
