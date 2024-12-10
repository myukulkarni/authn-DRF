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

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from .models import Product, Comment, Like, Rating
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Decorator to ensure the user is logged in
@method_decorator(login_required, name='dispatch')
class CommentView(View):
    def post(self, request, product_id):
        # Create a new comment
        product = get_object_or_404(Product, id=product_id)
        content = request.POST.get('content')

        if content:
            comment = Comment.objects.create(
                user=request.user,
                product=product,
                content=content
            )
            return JsonResponse({'message': 'Comment created successfully!', 'comment_id': comment.id}, status=201)
        else:
            return JsonResponse({'error': 'Content is required!'}, status=400)
        
        
def get(self, request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comment_set.all()  # Retrieve related comments
    comment_list = [{
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at,
    } for comment in comments]
    return JsonResponse({'comments': comment_list}, status=200)


# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import Product, Like


class LikeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            # Get the product
            product = Product.objects.get(id=product_id)

            # Check if the user has already liked the product
            like, created = Like.objects.get_or_create(user=request.user, product=product)

            if not created:
                # If the like already exists, the user is unliking the product
                like.delete()
                product.like_count = F('like_count') - 1
                is_liked = False
            else:
                # Otherwise, the user is liking the product
                product.like_count = F('like_count') + 1
                is_liked = True

            # Save the product and refresh to get the actual updated count
            product.save()
            product.refresh_from_db()

            return Response({
                "message": "Product liked." if created else "Product unliked.",
                "like_count": product.like_count,
                "is_liked": is_liked  # Include this field
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error liking product: {str(e)}")
            return Response({"error": "Failed to like the product."}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from rest_framework import status

class LikedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Fetch all products liked by the authenticated user
        liked_products = Product.objects.filter(like__user=user)

        # Prepare the list of liked products as dictionaries
        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),  # Convert Decimal to string for JSON
                'image1_url': request.build_absolute_uri(product.image1.url) if product.image1 else None,
                'like_count': product.like_count,  # Assuming you have a like_count field
                'is_liked': True,
            }
            for product in liked_products
        ]

        return Response({'liked_products': products_data}, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class RatingView(View):
    def post(self, request, product_id):
        # Create or update the rating for a product
        product = get_object_or_404(Product, id=product_id)
        rating_value = request.POST.get('rating')

        if not rating_value:
            return JsonResponse({'error': 'Rating value is required!'}, status=400)

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5!'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating value!'}, status=400)

        # Check if the user has already rated the product
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating_value}
        )

        return JsonResponse({'message': 'Rating submitted successfully!', 'rating': rating.rating}, status=201)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Product, Purchase

class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        products = request.data.get("products", [])  # Expected format: [{"id": 1, "quantity": 2}, ...]

        if not products:
            return Response({"error": "No products provided."}, status=400)

        purchases = []
        for item in products:
            try:
                product = Product.objects.get(id=item["id"])
                quantity = item.get("quantity", 1)
                if quantity < 1:
                    return Response({"error": "Quantity must be at least 1."}, status=400)

                purchase = Purchase(user=user, product=product, quantity=quantity)
                purchases.append(purchase)
            except Product.DoesNotExist:
                return Response({"error": f"Product with id {item['id']} not found."}, status=404)

        # Bulk create all purchases
        Purchase.objects.bulk_create(purchases)
        return Response({"message": "Purchase successful."}, status=201)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Purchase

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Fetch all purchases made by the user
        purchases = Purchase.objects.filter(user=user).select_related('product')
        
        # Prepare the data to return
        order_history = [
            {
                "product_id": purchase.product.id,
                "product_name": purchase.product.name,
                "quantity": purchase.quantity,
                "purchased_at": purchase.purchased_at.strftime('%Y-%m-%d %H:%M:%S')  # Assuming you have a `created_at` field
            }
            for purchase in purchases
        ]

        return Response({"order_history": order_history}, status=200)
