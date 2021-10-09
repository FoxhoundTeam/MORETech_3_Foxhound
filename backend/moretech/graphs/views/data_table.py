import json

from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.core import serializers

from ..models import DataTable
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
        data_tables = []
        for data_table in DataTable.objects.all():
            data_tables.append({
                'id': data_table.id,
                'name': data_table.name,
                'description': data_table.description,
                'icon': data_table.icon,
                'source': data_table.source,
                'size': data_table.size,
                'tag': data_table.tag,
                'loaddate': data_table.loaddate,
            })
        return get_success_response({
            'data_table': data_tables,
        })
