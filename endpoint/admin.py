# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import OCREndpoint, Task
from .models import Company, CaibaoFile


class EndpointAdmin(admin.ModelAdmin):
    
    list_display = ('pk', 'url', 'capacity', 'current_load')

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
    readonly_fields = ('file_link',)

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
        # "task_id",
        "file_name",
        "status",
        "file_link",
        "source_file_link", 
        "biz_type",
        "created_at",
        "updated_at",
        "short_message"
    )

    search_fields = ("status", "biz_type", "message")
    list_filter = ("status", "biz_type")
    readonly_fields = ("source_file_link", "file_link", "file_name", "short_message")

    # Create a clickable download link for the file field
    def file_link(self, obj):
        if obj.file:
            # Assuming the file is accessible via the URL field of the FileField
            # No preceding '/' for file.url
            return format_html('<a href="{}" download>Download</a>', obj.file.url)
        return "No file"

    file_link.allow_tags = True
    file_link.short_description = "Target File"


    def source_file_link(self, obj):
        # Get the admin URL for the related Author object
        if obj.source_file:
            # link = reverse("admin:endpoint_caibaofile_change", args=[obj.source_file.id])
            # return format_html('<a href="{}">{}</a>', link, obj.source_file.id)
            return format_html('<a href="/{}" download>Download</a>', obj.source_file.file_path)
        return "No file"
    
    # Optional: Add a nicer column header name
    file_link.allow_tags = True
    source_file_link.short_description = 'Source File'

    
    def short_message(self, obj):
        if obj.message:
            return obj.message[:100]
    short_message.short_description = 'Message'
    
    
    def get_file_name(self, obj):
        if obj.source_file:
            return obj.source_file.file_path.split('/')[-1]
        return "No file"

admin.site.register(OCREndpoint, EndpointAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CaibaoFile, CaibaoFileAdmin)
admin.site.register(Task, TaskAdmin)


