import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Mobile
from .serializers import MobileSerializer
from django.core.exceptions import PermissionDenied

CUSTOMER_SERVICE_URL = "http://localhost:8000/customer"

def is_admin(request):
    try:
        response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
        if response.status_code != 200:
            return False  
        
        customer_data = response.json()
        return customer_data.get("customer_type", "").lower() == "admin"

    except Exception as e:
        print(f"Error in is_admin: {e}")
        return False

@api_view(['POST'])
def create_mobile(request):
    if not is_admin(request):
         raise PermissionDenied("You do not have permission to perform this action.")
    
    serializer = MobileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_mobile(request, mobile_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")

    try:
        mobile = Mobile.objects.get(id=mobile_id)
    except Mobile.DoesNotExist:
        return Response({"error": "Mobile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MobileSerializer(mobile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Mobile updated successfully!", "mobile": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_mobile(request, mobile_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    try:
        mobile = Mobile.objects.get(id=mobile_id)

        if mobile.image and mobile.image.grid_id:
            mobile.image.delete()

        mobile.delete()
        return Response({"message": "Mobile deleted successfully"}, status=204)
    except Mobile.DoesNotExist:
        return Response({"error": "Mobile not found"}, status=404)

@api_view(['GET'])
def get_single_mobile(request, mobile_id):
    try:
        mobile = Mobile.objects.get(id=mobile_id)
        serializer = MobileSerializer(mobile)
        return Response(serializer.data, status=200)
    except Mobile.DoesNotExist:
        return Response({"error": "Mobile not found"}, status=404)

@api_view(['GET'])
def get_all_mobiles(request):
    mobiles = Mobile.objects.all()
    serializer = MobileSerializer(mobiles, many=True)
    return Response(serializer.data, status=200)


