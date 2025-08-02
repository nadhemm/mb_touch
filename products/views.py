from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Product, Order, OrderItem
import json


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        items = data.get('items', [])

        if not customer_name or not customer_phone or not items:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        with transaction.atomic():
            # Calculate total amount
            total_amount = 0
            order_items = []

            for item in items:
                product = get_object_or_404(Product, id=item['product_id'])
                quantity = int(item['quantity'])
                price = product.price
                total_amount += quantity * price
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })

            # Create order
            order = Order.objects.create(
                customer_name=customer_name,
                customer_phone=customer_phone,
                total_amount=total_amount
            )

            # Create order items
            for item_data in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )

            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': 'Order created successfully! We will call you soon.'
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# API endpoint to get products as JSON
def api_products(request):
    products = Product.objects.filter(is_active=True)
    products_data = []

    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'image': product.image.url if product.image else None
        })

    return JsonResponse({'products': products_data})
