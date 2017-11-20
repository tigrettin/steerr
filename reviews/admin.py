from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Car, CarUS, Review, SuggestedPicture


class CarResource(resources.ModelResource):
    class Meta:
        model = Car


class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
    search_fields = ('make', 'years',)

 
class CarUSResource(resources.ModelResource):
    class Meta:
        model = CarUS


class CarUSAdmin(ImportExportModelAdmin):
    resource_class = CarUSResource
    search_fields = ('make', 'model', 'trim',)



admin.site.register(Car, CarAdmin)
admin.site.register(CarUS, CarUSAdmin)
admin.site.register(Review)
admin.site.register(SuggestedPicture)