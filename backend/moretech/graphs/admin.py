from django.contrib import admin

# Register your models here.
from .models import DataTable, Feature, Operation


@admin.register(DataTable)
class DataTableRegistered(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Feature)
class FunctionsRegistered(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Operation)
class OperationRegistered(admin.ModelAdmin):
    list_display = ["name"]