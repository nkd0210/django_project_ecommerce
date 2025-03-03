import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

CUSTOMER_SERVICE_URL = "http://localhost:8000/customer"
CART_SERVICE_URL = "http://localhost:8000/cart"
PAYMENT_SERVICE_URL = "http://localhost:8000/paying"
SHIPPING_SERVICE_URL = "http://localhost:8000/shipping"

@api_view(['POST'])
def create_order(request):
    """
    {
        "products": [
            {
                "product_type": "book",
                "product_id": "67bb1bf39fe18e871469f704",
                "quantity": 1,
                "price": 12.99
            }
        ],
        "payment": {
            "amount": 12.99,
            "method": "credit_card"
        },
        "shipping": {
            "recipient_name": "Kim Dungx",
            "recipient_phone": "0991234562",
            "address": "123 Lac Long Quan, Tay Ho, Ha Noi",
            "carrier": "j&t"
        }
    }
    """

    customer_id = request.session.get('user_id') 
    if not customer_id:
        return Response({"error": "User not logged in"}, status=401)

    data = request.data
    products = data.get("products", [])
    payment_info = data.get("payment", {})
    shipping_info = data.get("shipping", {})
    carrier = shipping_info.get("carrier", "j&t")

    # Kiểm tra dữ liệu hợp lệ
    if not products:
        return Response({"error": "No products provided"}, status=400)
    if not payment_info:
        return Response({"error": "Payment information is required"}, status=400)
    if not shipping_info:
        return Response({"error": "Shipping information is required"}, status=400)

    try:
        with transaction.atomic():
            # Lấy thông tin giỏ hàng
            cart_response = requests.get(f"{CART_SERVICE_URL}/get_customer_cart", cookies=request.COOKIES)
            if cart_response.status_code != 200:
                return Response({"error": "Failed to retrieve cart"}, status=cart_response.status_code)

            # Tính tổng tiền đơn hàng
            total_price = sum(p['price'] * p['quantity'] for p in products)

            # Tạo đơn hàng
            order = Order.objects.create(
                customer_id=customer_id,
                total_price=total_price,
                status="pending",
                is_paid=False
            )

            # Xử lý từng sản phẩm và loại bỏ khỏi giỏ hàng
            for product in products:
                requests.post(
                    f"{CART_SERVICE_URL}/remove_item_in_cart",
                    json={
                        "product_type": product["product_type"],
                        "product_id": product["product_id"],
                        "quantity": product["quantity"]
                    },
                    cookies=request.COOKIES
                )

                # Thêm sản phẩm vào đơn hàng
                OrderItem.objects.create(
                    order=order,
                    product_type=product["product_type"],
                    product_id=product["product_id"],
                    quantity=product["quantity"],
                    price=product["price"]
                )

            # Tạo thanh toán
            payment_response = requests.post(
                f"{PAYMENT_SERVICE_URL}/create_payment",
                json={"order_id": order.id, "amount": payment_info["amount"], "method": payment_info["method"]},
                cookies=request.COOKIES
            )
            if payment_response.status_code != 201:
                raise Exception("Failed to create payment")

            # Tạo thông tin giao hàng
            shipping_response = requests.post(
                f"{SHIPPING_SERVICE_URL}/create_shipping",
                json={
                    "order_id": order.id,
                    "recipient_name": shipping_info["recipient_name"],
                    "recipient_phone": shipping_info["recipient_phone"],
                    "address": shipping_info["address"],
                    "carrier": carrier
                },
                cookies=request.COOKIES
            )
            if shipping_response.status_code != 201:
                raise Exception("Failed to create shipping")

            return Response({"message": "Order created successfully", "order_id": order.id}, status=201)

    except Exception as e:
        # Rollback transaction nếu có lỗi
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_customer_orders(request):
    customer_id = request.session.get('user_id')
    if not customer_id:
        return Response({"error": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    # Lấy danh sách order của người dùng
    orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
    
    # Serialize dữ liệu
    serializer = OrderSerializer(orders, many=True)
    
    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_order(request, order_id):
    customer_response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
    if customer_response.status_code != 200:
        return Response({"error": "Failed to retrieve customer details"}, status=customer_response.status_code)

    customer_data = customer_response.json()
    customer_type_name = customer_data.get("customer_type", "")

    if customer_type_name != "admin":
        return Response({"error": "Permission denied. Only admin can delete orders."}, status=status.HTTP_403_FORBIDDEN)

    # Tìm order và xóa nó
    order = get_object_or_404(Order, id=order_id)
    try:
        with transaction.atomic():
            payment_response = requests.delete(
                f"{PAYMENT_SERVICE_URL}/delete_payment/{order_id}",
                cookies=request.COOKIES
            )
            if payment_response.status_code != 200:
                raise Exception(f"Failed to delete payment for order {order_id}")

            shipping_response = requests.delete(
                f"{SHIPPING_SERVICE_URL}/delete_shipping/{order_id}",
                cookies=request.COOKIES
            )
            if shipping_response.status_code != 200:
                raise Exception(f"Failed to delete shipping for order {order_id}")

            order.delete()

            return Response({"message": f"Order {order_id} and its related data have been deleted successfully."}, status=status.HTTP_200_OK)

    except Exception as e:
        # Bắt lỗi và trả về phản hồi
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_order_by_id(request, order_id):
    customer_response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
    if customer_response.status_code != 200:
        return Response({"error": "Failed to retrieve customer details"}, status=customer_response.status_code)

    try:
        customer_data = customer_response.json()  # Ensure JSON parsing
    except ValueError:
        return Response({"error": "Invalid response from customer service"}, status=500)

    user_id = customer_data.get("id")
    customer_type_name = customer_data.get("customer_type", "")

    # Lấy đơn hàng
    order = get_object_or_404(Order, id=order_id)

    # Nếu người dùng không phải admin và không phải chủ sở hữu của order thì từ chối
    if customer_type_name  != "admin" and order.customer_id != user_id:
        return Response({"error": "Permission denied. You can only view your own orders."}, status=status.HTTP_403_FORBIDDEN)

    # Serialize và trả về dữ liệu đơn hàng
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_order(request, order_id):
    customer_response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
    if customer_response.status_code != 200:
        return Response({"error": "Failed to retrieve customer details"}, status=customer_response.status_code)

    customer_data = customer_response.json()
    customer_type_name = customer_data.get("customer_type", "")

    if customer_type_name != "admin":
        return Response({"error": "Permission denied. Only admin can update orders."}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Lấy thông tin order theo order_id
        order = Order.objects.get(id=order_id)

        # Lấy dữ liệu từ request
        data = request.data
        new_status = data.get("status", order.status)  # Nếu không có status, giữ nguyên giá trị cũ
        is_paid = data.get("is_paid", order.is_paid)  # Nếu không có is_paid, giữ nguyên giá trị cũ

        # Kiểm tra giá trị hợp lệ cho status
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return Response({"error": f"Invalid status. Valid values are: {valid_statuses}"}, status=400)

        # Cập nhật các trường
        order.status = new_status
        order.is_paid = is_paid
        order.save()  # Lưu thay đổi vào cơ sở dữ liệu

        return Response(
            {"message": "Order updated successfully", "order": {
                "id": order.id,
                "customer_id": order.customer_id,
                "total_price": str(order.total_price),
                "status": order.status,
                "is_paid": order.is_paid,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            }},
            status=200
        )
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['GET'])
def get_all_orders(request):
    customer_response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
    if customer_response.status_code != 200:
        return Response({"error": "Failed to retrieve customer details"}, status=customer_response.status_code)

    customer_data = customer_response.json()
    customer_type_name = customer_data.get("customer_type", "")

    if customer_type_name != "admin":
        return Response({"error": "Permission denied. Only admin can delete orders."}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Lấy tất cả các đơn hàng
        orders = Order.objects.all()

        # Sử dụng serializer để serialize danh sách đơn hàng
        serializer = OrderSerializer(orders, many=True)

        return Response({"orders": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
