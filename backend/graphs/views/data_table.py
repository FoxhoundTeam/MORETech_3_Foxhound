import json
from rest_framework.views import APIView

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
                'tags': json.loads(data_table.tag),
                'loaddate': data_table.loaddate,
                'fields': json.loads(data_table.fields),
                'price': data_table.price,
            })
        return get_success_response({
            'data_table': data_tables,
        })
