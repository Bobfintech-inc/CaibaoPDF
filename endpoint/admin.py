# admin.py
from django.contrib import admin
from .models import Task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Company, CaibaoFile

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'priority', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('priority',)
    ordering = ('-priority',)

class CaibaoFileAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'hash_digest', 'company', 'priority', 'created_at', 'updated_at')
    search_fields = ('file_path', 'hash_digest')
    list_filter = ('priority', 'company')
    ordering = ('-priority',)


# Registering the models with their respective admin classes
admin.site.register(Company, CompanyAdmin)
admin.site.register(CaibaoFile, CaibaoFileAdmin)

class TaskAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = (
        "task_id",
        "status",
        "message",
        "biz_type",
        "file_name",
        "updated_at",
    )

    # Fields that can be used for searching in the admin panel
    search_fields = ("task_id", "status", "biz_type")

    # Add filters for filtering tasks by status and biz_type
    list_filter = ("status", "biz_type")

    # Make file field clickable for easy file download
    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}">Download</a>'
        return "No file"

    file_link.allow_tags = True
    file_link.short_description = "File"

    # Optionally, make `file_link` a part of `list_display`
    list_display = (
        "task_id",
        "status",
        "message",
        "biz_type",
        "file_name",
        "updated_at",
        "file_link",
    )


# Register the model and its admin configuration
admin.site.register(Task, TaskAdmin)


# Create the interval schedule for 1.5 minutes (90 seconds)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=90,  # Interval in seconds (90 seconds = 1.5 minutes)
    period=IntervalSchedule.SECONDS,
)

# Create a periodic task that will execute the `update_task_status` task
PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Submit OCR Task, Every 1.5 Minutes",
    task="endpoint.tasks.submit_ocr_task",
)


# class PeriodicTaskAdmin(admin.ModelAdmin):
#     model = PeriodicTask
#     list_display = ('name', 'interval', 'enabled', 'last_run_at', 'date_changed')

# admin.site.register(PeriodicTask, PeriodicTaskAdmin)
