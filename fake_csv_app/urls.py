from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.data_schemas_page, name='schemas'),
    path('data_sets/<int:schema_id>', views.data_sets_page, name='datasets'),
    path('create_schema/', views.SchemaCreate.as_view(), name='create_schema'),
    path('update_schema/<int:pk>/', views.SchemaUpdate.as_view(), name='update_schema'),
    path('delete_schema/<int:schema_id>', views.delete_schema_view, name='delete_schema'),
    path('create_dataset/', views.create_dataset, name='create_dataset'),
    path('get_last_dataset/<int:schema_id>', views.get_last_dataset_view, name='get_last_dataset'),
    path('delete_column/<int:column_id>/', views.delete_column_view, name='delete_column'),
]
