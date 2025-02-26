# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Company, CaibaoFile



class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'priority', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('priority',)
    ordering = ('-priority',)

# CaibaoFile admin setup with downloadable link for file_path
class CaibaoFileAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'file_link', 'hash_digest', 'company', 'priority', 'created_at', 'updated_at')
    search_fields = ('file_path', 'hash_digest')
    list_filter = ('priority', 'company')
    ordering = ('-priority',)

    # Create a clickable download link for file_path
    def file_link(self, obj):
        if obj.file_path:
            # Assuming file_path is a valid URL or path to the file
            # prefix '/' for file_path
            return format_html('<a href="/{}" download>Download</a>', obj.file_path)
        return "No file"

    file_link.allow_tags = True
    file_link.short_description = "File"

# Task admin setup with downloadable link for file (assuming Task has a file field)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_id",
        "status",
        "message",
        "biz_type",
        "file_name",
        "updated_at",
        "source_file",
        "file_link",  # Add the downloadable link to list_display
    )

    search_fields = ("task_id", "status", "biz_type")
    list_filter = ("status", "biz_type")

    # Create a clickable download link for the file field
    def file_link(self, obj):
        if obj.file:
            # Assuming the file is accessible via the URL field of the FileField
            # No preceding '/' for file.url
            return format_html('<a href="{}" download>Download</a>', obj.file.url)
        return "No file"

    file_link.allow_tags = True
    file_link.short_description = "File"


admin.site.register(Company, CompanyAdmin)
admin.site.register(CaibaoFile, CaibaoFileAdmin)
admin.site.register(Task, TaskAdmin)



# clear IntervalSchedule table 
IntervalSchedule.objects.all().delete()
# Create the interval schedule for 1.5 minutes (90 seconds)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=90,  # Interval in seconds (90 seconds = 1.5 minutes)
    period=IntervalSchedule.SECONDS,
)

# clear PeriodicTask table
PeriodicTask.objects.all().delete()
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
