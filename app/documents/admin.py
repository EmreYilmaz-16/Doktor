from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'original_filename', 'category', 'uploaded_by', 'created_at')
    list_filter = ('category',)
    search_fields = ('patient__name', 'patient__surname', 'original_filename')
