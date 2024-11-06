# from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

@csrf_exempt
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data['imageUrl']  # Retrieve the image URL from the request
        )
        product.save()
        return JsonResponse({"message": "Product created successfully!"})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
    
def get_products(request):
    products = Product.objects.all()
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "image": product.image  # This will be the URL of the image
        }
        for product in products
    ]
    return JsonResponse(product_list, safe=False)