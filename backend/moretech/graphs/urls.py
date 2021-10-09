from django.urls import path
from .views import data_tabels, functions, join_table, operations

app_name = "graphs"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('data_tabels', data_tabels.UserView.as_view()),
    path('functions', functions.UserView.as_view()),
    path('join_table', join_table.UserView.as_view()),
    path('operations', operations.UserView.as_view()),
]
