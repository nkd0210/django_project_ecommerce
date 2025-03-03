import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shipping

ORDER_SERVICE_URL = "http://localhost:8000/order"

@api_view(['POST'])
def create_shipping(request):
    data = request.data
    order_id = data.get("order_id")
    recipient_name = data.get("recipient_name")
    recipient_phone = data.get("recipient_phone")
    address = data.get("address")
    carrier = data.get("carrier", "j&t")

    if not order_id or not recipient_name or not recipient_phone or not address:
        return Response({"error": "Invalid shipping data"}, status=400)

    order_url = f"{ORDER_SERVICE_URL}/get_order_by_id/{order_id}"
    order_response = requests.get(order_url, cookies=request.COOKIES)

    if order_response.status_code != 200:
        return Response(order_response.json(), status=order_response.status_code)

    Shipping.objects.create(
        order_id=order_id,
        recipient_name=recipient_name,
        recipient_phone=recipient_phone,
        address=address,
        carrier=carrier
    )

    return Response({"message": "Shipping created successfully"}, status=201)

@api_view(['DELETE'])
def delete_shipping(request, order_id):
    try:
        # Tìm thông tin vận chuyển dựa trên order_id
        shipping = Shipping.objects.get(order_id=order_id)
        shipping.delete()  # Xóa thông tin vận chuyển

        return Response({"message": "Shipping deleted successfully"}, status=200)
    except Shipping.DoesNotExist:
        return Response({"error": "Shipping not found"}, status=404)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['PUT'])
def update_shipping(request, order_id):
    try:
        # Tìm thông tin vận chuyển dựa trên order_id
        shipping = Shipping.objects.get(order_id=order_id)

        # Lấy dữ liệu từ request
        data = request.data
        recipient_name = data.get("recipient_name", shipping.recipient_name)  # Giữ nguyên nếu không truyền
        recipient_phone = data.get("recipient_phone", shipping.recipient_phone)
        address = data.get("address", shipping.address)
        carrier = data.get("carrier", shipping.carrier)

        # Cập nhật thông tin vận chuyển
        shipping.recipient_name = recipient_name
        shipping.recipient_phone = recipient_phone
        shipping.address = address
        shipping.carrier = carrier
        shipping.save()  # Lưu thay đổi vào cơ sở dữ liệu

        return Response(
            {"message": "Shipping updated successfully", "shipping": {
                "order_id": shipping.order_id,
                "recipient_name": shipping.recipient_name,
                "recipient_phone": shipping.recipient_phone,
                "address": shipping.address,
                "carrier": shipping.carrier
            }},
            status=200
        )
    except Shipping.DoesNotExist:
        return Response({"error": "Shipping not found"}, status=404)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

