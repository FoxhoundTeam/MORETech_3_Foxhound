import json

from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.core import serializers

from ..models import JoinTable
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
        join_tables = []
        for join_table in JoinTable.objects.all():
            join_tables.append({
                'name': join_table.name,
                'description': join_table.description,
                'icon': join_table.icon,
                'inputs': join_table.inputs,
                'outputs': join_table.outputs,
            })
        return get_success_response({
            'data_tables': join_tables,
        })
