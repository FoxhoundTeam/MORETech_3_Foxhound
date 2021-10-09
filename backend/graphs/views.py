import json

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .models import Operation, Feature, DataTable
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
        operations = []
        for operation in Operation.objects.all():
            operations.append({
                'name': operation.name,
                'description': operation.description,
                'number_of_elements': operation.number_of_elements,
                'icon': operation.icon,
                'type_elements': operation.type_elements,
                'type_output': operation.type_output,
                'json_data': operation.json_data,
            })
        features = []
        for feature in Feature.objects.all():
            features.append({
                'name': function.name,
                'description': function.description,
                'params': function.params,
                'icon': function.icon,
                'owner': function.owner,
                'owner_icon': function.owner_icon,
                'type_output': function.type_output,
                'price': function.price,
            })
        data_tables = []
        for data_table in DataTable.objects.all():
            data_tables.append({
                'name': data_table.name,
                'description': data_table.description,
                'icon': data_table.icon,
                'owner': data_table.owner,
                'owner_icon': data_table.owner_icon,
                'columns': data_table.columns,
                'price': data_table.price,
            })
        return get_success_response({
            'operations': operations,
            'feature': feature,
            'data_tables': data_tables,
        })
