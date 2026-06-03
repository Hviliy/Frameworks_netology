from django.contrib import admin

from workshops.models import Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("title", "starts_at", "capacity", "created_by")
    list_filter = ("starts_at",)
    search_fields = ("title", "description")
