import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from .models import Shoes
from .serializers import ShoesSerializer

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
def create_shoe(request):
    if not is_admin(request):
         raise PermissionDenied("You do not have permission to perform this action.")
    
    serializer = ShoesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_shoe(request, shoe_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")

    try:
        shoe = Shoes.objects.get(id=shoe_id)
    except Shoes.DoesNotExist:
        return Response({"error": "Shoe not found"}, status=404)
    
    serializer = ShoesSerializer(shoe, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Shoe updated successfully!", "shoe": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_shoe(request, shoe_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    try:
        shoe = Shoes.objects.get(id=shoe_id)

        if shoe.image and shoe.image.grid_id:
            shoe.image.delete()

        shoe.delete()
        return Response({"message": "Shoe deleted successfully"}, status=204)
    except Shoes.DoesNotExist:
        return Response({"error": "Shoe not found"}, status=404)

@api_view(['GET'])
def get_single_shoe(request, shoe_id):
    try:
        shoe = Shoes.objects.get(id=shoe_id)
        serializer = ShoesSerializer(shoe)
        return Response(serializer.data, status=200)
    except Shoes.DoesNotExist:
        return Response({"error": "Shoe not found"}, status=404)

@api_view(['GET'])
def get_all_shoes(request):
    shoes = Shoes.objects.all()
    serializer = ShoesSerializer(shoes, many=True)
    return Response(serializer.data, status=200)
