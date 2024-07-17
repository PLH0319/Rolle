from django.urls import path
from . import views

urlpatterns = [
    path('operation/', views.OperationView.as_view(), name='operation'),
    path('api/delete/', views.delete_data, name='delete_data'),
    path('api/query/', views.query_data, name='query_data'),
    path('api/modify/', views.modify_data, name='modify_data'),
    # other urls
]