from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Car, Review


class CarResource(resources.ModelResource):

    class Meta:
        model = Car


class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
 

admin.site.register(Car, CarAdmin)
admin.site.register(Review)