from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home_inventory, name='home_inventory'),
    # View for all items
    path('inventory/all/', views.all_items, name='all_items'),
    path('<int:item_id>/', views.detail, name='detail'),
    path('<int:item_id>/update/', views.update_item, name='update_item'),
    path('inventory/add/', views.create_item, name='add_item'),
]