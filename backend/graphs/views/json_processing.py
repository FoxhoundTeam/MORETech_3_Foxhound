# Create your views here.
from rest_framework.views import APIView

from ..models import Operation, Feature, DataTable
from main.response_processing import get_success_response

def find_object(name):
    operations = Operation.objects.filter(name=name)
    if operations:
        operation = operations[0]
        return {
            "name": operation.name,
            "id": operation.id,
            "type": 'operation',
        }

    features = Feature.objects.filter(name=name)
    if features:
        features = features[0]
        return {
            "name": features.name,
            "id": features.id,
            "type": 'features',
        }

    data_tables = DataTable.objects.filter(name=name)
    if data_tables:
        data_table = data_tables[0]
        return {
            "name": data_table.name,
            "id": data_table.id,
            "type": 'data_table',
        }

    return {
        "name": name,
        "id": 'join',
        "type": 'join',
    }

class UserView(APIView):
    def post(self, request):
        data = request.data
        nodes = data['nodes']
        nodes_in_objects = {}
        output = {}
        for key, node in nodes.items():
            output[node['name']] = {}
            obj = find_object(node['name'])
            nodes_in_objects[key] = obj
            output[node['name']]['id'] = obj['id']
            output[node['name']]['type'] = obj['type']
            outputs = []
            for key1, output_o in node['outputs'].items():
                connections = output_o['connections']
                if connections:
                    for connection in connections:
                        outputs.append({
                            "node": connection['node'],
                            "name_field": connection['input'],
                        })

            inputs = []
            for key1, output_i in node['inputs'].items():
                connections = output_i['connections']
                if connections:
                    for connection in connections:
                        inputs.append({
                            "node": connection['node'],
                            "name_field": connection['output'],
                        })
            output[node['name']]['connections'] = {}
            output[node['name']]['connections']['inputs'] = inputs
            output[node['name']]['connections']['output'] = outputs

        for key, dates in output.items():
            connections = dates['connections']
            for input_data in connections['inputs']:
                if input_data.get('node'):
                    input_data['object_information'] = nodes_in_objects[str(input_data['node'])]
                    del input_data['node']
            for output_data in connections['output']:
                if output_data.get('node'):
                    output_data['object_information'] = nodes_in_objects[str(output_data['node'])]
                    del output_data['node']

        return get_success_response(output)

