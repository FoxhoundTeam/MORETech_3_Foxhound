import json

# Create your views here.
from rest_framework.views import APIView

from ..models import Operation
from main.response_processing import get_success_response

data = {
    'J': 'join',
    'O': 'operation',
    'F': 'filter',
    'T': 'output',
}


class UserView(APIView):
    def get(self, request):
        operations = []
        for operation in Operation.objects.all():
            operations.append({
                'name': operation.name,
                'icon': operation.icon,
                'type_': data.get(operation.type_element, 'join'),
                'many': operation.many,
                'inputs': json.loads(operation.inputs),
                'type_output': json.loads(operation.outputs),
            })
        return get_success_response({
            'operations': operations,
        })
