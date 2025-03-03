import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartItem
from .serializers import CartSerializer

BOOK_SERVICE_URL = "http://localhost:8000/book"
MOBILE_SERVICE_URL = "http://localhost:8000/mobile"
CLOTHES_SERVICE_URL = "http://localhost:8000/clothes"
SHOES_SERVICE_URL = "http://localhost:8000/shoes"

@api_view(['POST'])
def create_cart(request):
    customer_id = request.data.get('customer_id')

    if not customer_id:
        return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    cart = Cart.objects.create(customer_id=customer_id)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=201)

@api_view(['DELETE'])
def delete_cart(request, customer_id):
    try:
        cart = Cart.objects.filter(customer_id=customer_id).first()

        if not cart:
            return Response({'message': 'No cart found for this customer'}, status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_to_cart(request):
    """
    {
        "product_type": "book",
        "product_id": "67bb1bf39fe18e871469f704",
        "quantity": 1,
        "price": 12.99
    }
    """
    customer_id = request.session.get('user_id')
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    data = request.data
    product_type = data.get("product_type")  # Tên loại sản phẩm: book, shoes, clothes
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    price = data.get("price")

    service_urls = {
        "book": BOOK_SERVICE_URL + f"/get-single-book/{product_id}",
        "mobile": MOBILE_SERVICE_URL + f"/get_single_mobile/{product_id}",
        "clothes": CLOTHES_SERVICE_URL + f"/get_single_clothe/{product_id}",
        "shoes": SHOES_SERVICE_URL + f"/get_single_shoe/{product_id}"
    }
   
    if product_type in service_urls:
        response = requests.get(service_urls[product_type])
        if response.status_code != 200:
            return Response({"error": f"{product_type.capitalize()} not found"}, status=404)
        product_data = response.json()
        price = float(product_data.get("price", price))
    else:
        return Response({"error": "Invalid product type"}, status=400)

    # Lấy hoặc tạo giỏ hàng của khách hàng
    cart, _ = Cart.objects.get_or_create(customer_id=customer_id)

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_type=product_type,
        product_id=product_id,
        defaults={"quantity": quantity, "price": price},
    )

    if not created:
        # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"message": "Item added to cart successfully"}, status=201)

@api_view(['POST'])
def remove_from_cart(request):
    """
    {
        "product_type": "book",
        "product_id": "67bb1bf39fe18e871469f704"
    }
    """
    customer_id = request.session.get('user_id')  # Lấy customer_id từ session
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    data = request.data
    product_type = data.get("product_type")  # Tên loại sản phẩm: book, shoes, clothes
    product_id = data.get("product_id")

    # Kiểm tra xem giỏ hàng có tồn tại không
    try:
        cart = Cart.objects.get(customer_id=customer_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    # Kiểm tra xem sản phẩm có trong giỏ hàng không
    try:
        cart_item = CartItem.objects.get(cart=cart, product_type=product_type, product_id=product_id)
        cart_item.delete()
        return Response({"message": "Item removed from cart successfully"}, status=200)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart"}, status=404)

@api_view(['POST'])
def update_item_in_cart(request):
    """
    {
        "product_type": "book",
        "product_id": "67bb1bf39fe18e871469f704",
        "quantity": 3
    }
    """
    customer_id = request.session.get('user_id')  # Lấy customer_id từ session
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    data = request.data
    product_type = data.get("product_type")  # Tên loại sản phẩm: book, shoes, clothes
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if quantity <= 0:
        return Response({"error": "Quantity must be greater than 0"}, status=400)

    service_urls = {
        "book": BOOK_SERVICE_URL + f"/get-single-book/{product_id}",
        "mobile": MOBILE_SERVICE_URL + f"/get_single_mobile/{product_id}",
        "clothes": CLOTHES_SERVICE_URL + f"/get_single_clothe/{product_id}",
        "shoes": SHOES_SERVICE_URL + f"/get_single_shoe/{product_id}"
    }

    if product_type in service_urls:
        response = requests.get(service_urls[product_type])
        if response.status_code != 200:
            return Response({"error": f"{product_type.capitalize()} not found"}, status=404)
    else:
        return Response({"error": "Invalid product type"}, status=400)

    # Kiểm tra xem giỏ hàng có tồn tại không
    try:
        cart = Cart.objects.get(customer_id=customer_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    # Kiểm tra xem sản phẩm có trong giỏ hàng không
    try:
        cart_item = CartItem.objects.get(cart=cart, product_type=product_type, product_id=product_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart"}, status=404)

    # Cập nhật quantity
    cart_item.quantity = quantity
    cart_item.save()

    # Nếu quantity = 0, xóa sản phẩm khỏi giỏ hàng
    if cart_item.quantity == 0:
        cart_item.delete()
        return Response({"message": "Item removed from cart successfully because quantity is 0"}, status=200)

    return Response({"message": "Item quantity updated successfully"}, status=200)

@api_view(['GET'])
def get_customer_cart(request):
    customer_id = request.session.get('user_id')  # Lấy customer_id từ session
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    # Lấy hoặc tạo giỏ hàng của khách hàng
    try:
        cart = Cart.objects.get(customer_id=customer_id)
    except Cart.DoesNotExist:
        return Response({"message": "Cart is empty"}, status=404)

    # Serialize giỏ hàng
    serializer = CartSerializer(cart)

    return Response(serializer.data, status=200)

# hàm này để xử lý khi order thì sẽ trừ đi số lượng tương ứng trong cart
@api_view(['POST'])
def remove_item_in_cart(request):
    customer_id = request.session.get('user_id')
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    data = request.data
    product_type = data.get("product_type")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_type or not product_id or not quantity:
        return Response({"error": "Invalid request data"}, status=400)

    cart = Cart.objects.filter(customer_id=customer_id).first()
    if not cart:
        return Response({"error": "Cart not found"}, status=404)

    cart_item = CartItem.objects.filter(cart=cart, product_type=product_type, product_id=product_id).first()
    if not cart_item:
        return Response({"error": "Item not found in cart"}, status=404)

    if cart_item.quantity > quantity:
        cart_item.quantity -= quantity
        cart_item.save()
    else:
        cart_item.delete()

    return Response({"message": "Item removed successfully"}, status=200)