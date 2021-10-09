from django.urls import path
from .views import data_table, feature, operations, json_processing

app_name = "graphs"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('data_table', data_table.UserView.as_view()),
    path('feature', feature.UserView.as_view()),
    path('operation', operations.UserView.as_view()),
    path('json', json_processing.UserView.as_view()),
]
