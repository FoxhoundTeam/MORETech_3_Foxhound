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
                'icon': operation.icon,
                'type_': operation.type_,
                'many': operation.many,
                'inputs': json.load(operation.inputs),
                'type_output': json.load(operation.outputs),
            })
        return get_success_response({
            'operations': operations,
        })
