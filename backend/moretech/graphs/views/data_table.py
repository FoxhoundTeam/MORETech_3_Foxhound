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
        functions = []
        for data_table in DataTable.objects.all():
            functions.append({
                'id': data_table.id,
                'name': data_table.name,
                'icon': data_table.icon,
                'owner': data_table.owner,
                'owner_icon': data_table.owner_icon,
                'description': data_table.description,
                'fields': json.loads(data_table.fields),
                'price': data_table.price,
            })
        return get_success_response({
            'functions': functions,
        })

    def post(self, request):
        data = request.data
        name = data['name']
        description = data['description']
        params = data['params']
        icon = data['icon']
        owner = data['owner']
        owner_icon = data['owner_icon']
        type_output = data['type_output']
        price = data['price']
        function = Functions.objects.create(
            name=name,
            description=description,
            params=params,
            icon=icon,
            owner=owner,
            owner_icon=owner_icon,
            type_output=type_output,
            price=price,
        )
        function.save()
        get_success_response({
            "status": "ok",
        })

    def put(self, request):
        data = request.data
        name = data['name']
        description = data['description']
        params = data['params']
        icon = data['icon']
        owner = data['owner']
        owner_icon = data['owner_icon']
        type_output = data['type_output']
        price = data['price']
        function = Functions.objects.filter(data['id'])[0]

        function.name = name
        function.description = description
        function.params = params
        function.icon = icon
        function.owner = owner
        function.owner_icon = owner_icon
        function.type_output = type_output
        function.price = price

        function.save()

        get_success_response({
            "status": "ok",
        })
