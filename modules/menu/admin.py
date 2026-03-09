from .models import Option, Section
from django.contrib import admin


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', )
    list_display_links = ('name', )
    search_fields = ('name', )
    ordering = ('id','name',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'title', 'url', 'target', )
    list_display_links = ('title', )
    list_filter = ('roles', 'section', )
    search_fields = ('title', 'url',)
    ordering = ('id', 'title', )
    filter_horizontal = ('roles',)
