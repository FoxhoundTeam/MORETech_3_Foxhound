from django.contrib import admin

# Register your models here.
from .models import DataTable, Functions, Operation, TypeElements


@admin.register(DataTable)
class DataTableRegistered(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Functions)
class FunctionsRegistered(admin.ModelAdmin):
    list_display = ("name", "owner", "price")


@admin.register(Operation)
class OperationRegistered(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(TypeElements)
class TypeElementsRegistered(admin.ModelAdmin):
    list_display = ["name"]
