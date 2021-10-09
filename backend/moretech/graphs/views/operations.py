import json

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from ..models import Operation
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
        return get_success_response({
            'operations': operations,
        })
