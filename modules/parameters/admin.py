from .models import FieldType, DocumentClassType, FieldOption
from django.contrib import admin


@admin.register(FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('name', )
    search_fields = ['id', 'name']


@admin.register(DocumentClassType)
class DocumentClassTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('name', )
    search_fields = ['id', 'name']

# class FieldOptionInline(admin.TabularInline):
#     model = FieldOption
#     extra = 1 
#     fields = ('value', 'title', ) 
#     inlines = [FieldOptionInline]

