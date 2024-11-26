from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('sales/', views.sale_list, name='sale_list'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('export/sales/', views.export_sales_csv, name='export_sales_csv'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('add-category/', views.add_category, name='add_category'),
]
