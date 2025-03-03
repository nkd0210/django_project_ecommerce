import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment

ORDER_SERVICE_URL = "http://localhost:8000/order"

@api_view(['POST'])
def create_payment(request):
    data = request.data
    order_id = data.get("order_id")
    amount = data.get("amount")
    method = data.get("method")

    if not order_id or not amount or not method:
        return Response({"error": "Invalid payment data"}, status=400)

    order_url = f"{ORDER_SERVICE_URL}/get_order_by_id/{order_id}"
    order_response = requests.get(order_url, cookies=request.COOKIES)

    if order_response.status_code != 200:
        return Response(order_response.json(), status=order_response.status_code)

    Payment.objects.create(order_id=order_id, amount=amount, method=method)

    return Response({"message": "Payment created successfully"}, status=201)

@api_view(['DELETE'])
def delete_payment(request, order_id):
    try:
        # Tìm thanh toán dựa trên order_id
        payment = Payment.objects.get(order_id=order_id)
        payment.delete()  # Xóa thanh toán

        return Response({"message": "Payment deleted successfully"}, status=200)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['PUT'])
def update_payment(request, order_id):
    try:
        payment = Payment.objects.get(order_id=order_id)

        # Lấy dữ liệu từ request
        data = request.data
        amount = data.get("amount", payment.amount)  # Nếu không truyền, giữ giá trị cũ
        method = data.get("method", payment.method)  # Nếu không truyền, giữ giá trị cũ

        # Cập nhật thông tin thanh toán
        payment.amount = amount
        payment.method = method
        payment.save()  # Lưu thay đổi vào cơ sở dữ liệu

        return Response(
            {"message": "Payment updated successfully", "payment": {
                "order_id": payment.order_id,
                "amount": payment.amount,
                "method": payment.method
            }},
            status=200
        )
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
