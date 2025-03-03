import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from .models import Clothes
from .serializers import ClothesSerializer

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
def create_clothe(request):
    if not is_admin(request):
         raise PermissionDenied("You do not have permission to perform this action.")
    
    serializer = ClothesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_clothe(request, clothe_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")

    try:
        clothe = Clothes.objects.get(id=clothe_id)
    except Clothes.DoesNotExist:
        return Response({"error": "Clothe not found"}, status=404)
    
    serializer = ClothesSerializer(clothe, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Clothe updated successfully!", "clothe": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_clothe(request, clothe_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    try:
        clothe = Clothes.objects.get(id=clothe_id)

        if clothe.image and clothe.image.grid_id:
            clothe.image.delete()

        clothe.delete()
        return Response({"message": "Clothe deleted successfully"}, status=204)
    except Clothes.DoesNotExist:
        return Response({"error": "Clothe not found"}, status=404)

@api_view(['GET'])
def get_single_clothe(request, clothe_id):
    try:
        clothe = Clothes.objects.get(id=clothe_id)
        serializer = ClothesSerializer(clothe)
        return Response(serializer.data, status=200)
    except Clothes.DoesNotExist:
        return Response({"error": "Clothe not found"}, status=404)

@api_view(['GET'])
def get_all_clothes(request):
    clothes = Clothes.objects.all()
    serializer = ClothesSerializer(clothes, many=True)
    return Response(serializer.data, status=200)
