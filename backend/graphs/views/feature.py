import json

from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.core import serializers

from ..models import Feature
from main.response_processing import get_success_response


class UserView(APIView):
    def get(self, request):
        functions = []
        for function in Feature.objects.all():
            functions.append({
                'id': function.id,
                'name': function.name,
                'data': json.loads(function.data),
                'user_id': function.user_id,
                'price': function.price,
            })
        return get_success_response({
            'feature': functions,
        })

    def post(self, request):
        data = request.data
        name = data['name']
        data_ = data['data']
        user_id = data['user_id']
        price = data['price']

        function = Feature.objects.create(
            name=name,
            data=data_,
            user_id=user_id,
            price=price,
        )
        function.save()
        return get_success_response({
            "status": "ok",
        })

    def put(self, request):
        data = request.data
        name = data['name']
        data_ = data['data']
        user_id = data['user_id']
        price = data['price']
        function = Feature.objects.filter(id=data['id'])[0]

        function.name = name
        function.data = data_
        function.user_id = user_id
        function.price = price

        function.save()

        return get_success_response({
            "status": "ok",
        })
