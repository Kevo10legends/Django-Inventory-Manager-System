
import csv

import numpy as np
from django.contrib import messages
# from django.http import JsonResponse
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product, Sale
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from .utils import forecast_revenue
from sklearn.linear_model import LinearRegression

from .forms import ProductForm, SaleForm, CategoryForm
from .models import Product, Sale


# def product_list(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 10)  # Show 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # search engine
#     query = request.GET.get('q')
#     if query:
#         products = Product.objects.filter(name__icontains=query)
#     else:
#         products = Product.objects.all()
#     paginator = Paginator(products, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'inventory/product_list.html', {'page_obj': page_obj, 'query': query})

def product_list(request):
    # Search engine: filter products based on query
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the products for the current page

    return render(request, 'inventory/product_list.html', {'page_obj': page_obj, 'query': query})




def sale_list(request):
    sales = Sale.objects.all()
    paginator = Paginator(sales, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/sale_list.html', {'sales': sales})

#analytic dashboard


def analytics_dashboard(request):
    # Product Performance
    top_products = Sale.objects.values('product__name').annotate(total_sales=Sum('quantity_sold')).order_by(
        '-total_sales')[:5]

    # Sales Trends
    sales_trends = Sale.objects.extra({'month': "strftime('%%m', date)"}).values('month').annotate(
        total_revenue=Sum('quantity_sold')).order_by('month')

    # Inventory Value
    inventory_value = Product.objects.aggregate(total_value=Sum('price'))

    data = Sale.objects.all()
    for record in data:
        record.quantity_sold = record.quantity  # Simulate the field in memory

    # Prepare context
    context = {
        'top_products': list(top_products),
        'sales_trends': list(sales_trends),
        'inventory_value': inventory_value['total_value'],
    }
#Forecasting Function
    forecast = forecast_revenue()
    context = {
        'forecast': forecast,
    }

    sales = Sale.objects.all()  # Check if this is returning any data
    if not sales.exists():
        print("No sales data available.")



    return render(request, 'inventory/analytics_dashboard.html', context)

#end analytic

#export data to csv

def export_sales_csv(request):
    sales = Sale.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Product', 'Quantity Sold', 'Date', 'Customer Name'])
    for sale in sales:
        writer.writerow([sale.product.name, sale.quantity_sold, sale.date, sale.customer_name])
    return response

#end export data to csv

#Create a Forecasting Function
def forecast_revenue():
    sales = Sale.objects.extra({'month': "strftime('%%m', date)"}).values('month').annotate(total_revenue=Sum('quantity_sold')).order_by('month')

    # Prepare data
    months = np.array([int(sale['month']) for sale in sales]).reshape(-1, 1)
    revenues = np.array([sale['total_revenue'] for sale in sales])

    # Train the model
    model = LinearRegression()
    model.fit(months, revenues)

    # Predict next 3 months
    future_months = np.array(range(months[-1][0] + 1, months[-1][0] + 4)).reshape(-1, 1)
    predictions = model.predict(future_months)

    return list(zip(future_months.flatten(), predictions))

#end Create a Forecasting Function

#Product forms


# Product Views
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')  # Adjust the redirect as needed
        else:
            messages.error(request, "Error adding product. Please check the form.")
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

# Sale Views
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sale added successfully!")
            return redirect('add_sale')  # Adjust the redirect as needed
        else:
            messages.error(request, "Failed to add Sale. Please check your input.")
    else:
        form = SaleForm()
    return render(request, 'inventory/add_sale.html', {'form': form})

# Category Views
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('add_product')  # Adjust the redirect as needed
        else:
            messages.error(request, "Failed to add Category. Please check your input.")
    else:
        form = CategoryForm()
    return render(request, 'inventory/add_category.html', {'form': form})

#end product