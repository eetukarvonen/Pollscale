"""
admin configure for scales-app
"""
from django.contrib import admin
from .models import Scale

admin.site.site_header = "Pollscale Admin"
admin.site.site_title = "Pollscale Admin Area"
admin.site.index_title = "Welcome to Pollscale admin area"

class ScaleInline(admin.TabularInline):
    """
    Tabular inline conf for scales
    """
    model = Scale
    extra = 1

class ScaleAdmin(admin.ModelAdmin):
    """
    Fields for scales
    """
    fieldsets = [(None, {'fields': ['scale_title', 'parent_scale', 'yays', 'nays']}),]
    inlines = [ScaleInline]

admin.site.register(Scale, ScaleAdmin)
