from django.contrib import admin
from .models import State, City, Country
from django.utils.html import format_html


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_capital', )
    list_display_links = ('name', )
    search_fields = ['id', 'name']

    def display_capital(self, obj):
        if obj.capital_code:
            try:
                city = City.objects.get(country=obj, code=obj.capital_code)
                return format_html('<span style="font-weight: bold;">{}</span>', city.name)
            except City.DoesNotExist:
                return format_html('<span style="color: red;" title="Capital no encontrada">{}</span>', obj.capital_code)
        return format_html('{}', '--')

    display_capital.short_description = 'Capital'

admin.site.register(Country, CountryAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ('code', 'short', 'name', 'display_capital', 'country', )
    list_display_links = ('code', 'name', )
    list_filter = ['country']
    search_fields = ['name', 'code']

    def display_capital(self, obj):
        if obj.capital_code:
            try:
                city = City.objects.get(country=obj.country, code=obj.capital_code)
                return format_html('<span style="font-weight: bold;">{}</span>', city.name)
            except City.DoesNotExist:
                return format_html('<span style="color: red;" title="Capital no encontrada">{}</span>', obj.capital_code)
        return format_html('{}', '--')

    display_capital.short_description = 'Capital'

admin.site.register(State, StateAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'state', 'country', )
    list_display_links = ('code', 'name', )
    list_filter = ['country', 'state']
    search_fields = ['name', 'code']
    
admin.site.register(City, CityAdmin)
