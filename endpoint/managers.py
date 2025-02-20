# fileapp/managers.py
from django.db import models


class OrderedManager(models.Manager):
    def get_queryset(self, field_name="priority", ascending=True):
        """
        Return objects ordered by a specific field.
        Args:
            field_name (str): The field by which to order.
            ascending (bool): Whether to order in ascending order.
        """
        order_direction = "" if ascending else "-"
        return super().get_queryset().order_by(f"{order_direction}{field_name}")
