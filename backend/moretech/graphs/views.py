from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class UserView(APIView):
    def get(self, request):
        pass
