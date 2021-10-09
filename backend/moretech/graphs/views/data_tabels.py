import json

from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.core import serializers

from .models import Operation, Functions, DataTable, OperationSerializer, FunctionsSerializer, DataTableSerializer
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
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
            'data_tables': data_tables,
        })
