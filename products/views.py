<<<<<<< HEAD
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

class CreateProductView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')

        # Get the images
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        if name and description and price:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image1=image1,
                image2=image2,
                image3=image3,
                image4=image4
            )
            return Response({
                "message": "Product created successfully!",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": str(product.price),
                    "image1": product.image1.url if product.image1 else None,
                    "image2": product.image2.url if product.image2 else None,
                    "image3": product.image3.url if product.image3 else None,
                    "image4": product.image4.url if product.image4 else None,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)



class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "image1": product.image1.url if product.image1 else None,
                "image2": product.image2.url if product.image2 else None,
                "image3": product.image3.url if product.image3 else None,
                "image4": product.image4.url if product.image4 else None,
            }
            for product in products
        ]
        return Response(product_list, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return Response({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'image1': product.image1.url if product.image1 else None,
            'image2': product.image2.url if product.image2 else None,
            'image3': product.image3.url if product.image3 else None,
            'image4': product.image4.url if product.image4 else None,
        }, status=status.HTTP_200_OK)


class UpdateProductView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        data = request.data

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)

        # Check for images and update them
        if 'image1' in request.FILES:
            product.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            product.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            product.image4 = request.FILES['image4']

        product.save()
        return Response({
            "message": "Product updated successfully.",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "image1": product.image1.url if product.image1 else None,
                "image2": product.image2.url if product.image2 else None,
                "image3": product.image3.url if product.image3 else None,
                "image4": product.image4.url if product.image4 else None,
            }
        }, status=status.HTTP_200_OK)


class DeleteProductView(APIView):
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        # Use 204 status code to indicate no content (successful deletion)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Cart


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        # Fetch product and ensure it exists
        product = get_object_or_404(Product, id=product_id)

        # Add or update the cart item
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return Response({"message": "Product added to cart successfully!"}, status=status.HTTP_200_OK)


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch user's cart items
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        # Prepare cart data for the response
        cart_data = [
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": str(item.product.price),
                "total": item.quantity * item.product.price,
                "product_image1": item.product.image1.url if item.product.image1 else None,
                "product_image2": item.product.image2.url if item.product.image2 else None,
                "product_image3": item.product.image3.url if item.product.image3 else None,
                "product_image4": item.product.image4.url if item.product.image4 else None,
            }
            for item in cart_items
        ]

        return Response(
            {"cart_items": cart_data, "total_price": total_price},
            status=status.HTTP_200_OK,
        )


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DeleteFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        user = request.user

        # Find the cart item for the user and the product
        cart_item = Cart.objects.filter(user=user, product__id=product_id).first()
        if not cart_item:
            return Response({"error": "Product not found in your cart."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the cart item
        cart_item.delete()
        return Response({"message": "Product removed from cart successfully."}, status=status.HTTP_200_OK)
=======
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
>>>>>>> 0da9d9919c2e0d416f821a2b0df46d12a2b74e28
