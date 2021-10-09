import json

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .models import Operation, Functions, DataTable
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
        operations = Operation.objects.all()
        functions = Functions.objects.all()
        data_tables = DataTable.objects.all()
        return get_success_response({
        })
