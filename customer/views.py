import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from .models import Customer, Address, CustomerType
from .serializers import CustomerSerializer, AddressSerializer

@api_view(['POST'])
def signup(request):
    data = request.data

    # Check if the email already exists
    if Customer.objects.filter(email=data.get('email')).exists():
        return Response({'error': 'Email is already registered'}, status=400)

    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        # Start a transaction to ensure both user and cart creation happen atomically
        try:
            with transaction.atomic():
                address_data = data.pop('address', None)

                # Save the customer to the database
                customer = serializer.save()

                if address_data and not Address.objects.filter(customer=customer).exists():
                    Address.objects.create(customer=customer, **address_data)

                # Create a Cart through API call
                cart_url = 'http://localhost:8000/cart/create_cart'  
                cart_data = {'customer_id': customer.id}
                cart_response = requests.post(cart_url, data=cart_data)

                if cart_response.status_code != 201:
                    raise Exception("Error creating cart")

            return Response({'message': 'User registered successfully'}, status=201)
        
        except Exception as e:
            # Rollback the customer and address creation if cart creation fails
            if 'customer' in locals():
                customer.delete()  # Delete the customer
            if 'address_data' in locals() and not Address.objects.filter(customer=customer).exists():
                Address.objects.filter(customer=customer).delete()  # Delete the address if it was created
            # Return the error response
            return Response({'error': str(e)}, status=400)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if not check_password(password, customer.password):
        return Response({'error': 'Incorrect password'}, status=401)

    request.session['user_id'] = customer.id
    serializer = CustomerSerializer(customer)

    return Response({'message': 'Login successful', 'user': serializer.data}, status=200)

@api_view(['POST'])
def logout(request):
    request.session.flush()
    return Response({'message': 'Logout successful'}, status=200)

@api_view(['GET'])
def getCustomer(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(Customer, id=user_id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=200)

@api_view(['PUT'])
def updateCustomer(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return Response({"error": "User ID not found in session."}, status=400)

    customer = get_object_or_404(Customer, id=user_id)
    data = request.data

    if "customer_type" in data:
        return Response({"error": "You do not have permission to update customer_type."}, status=403)

    if 'password' in data:
        data['password'] = make_password(data['password'])  # Ensure password is hashed

    customer_serializer = CustomerSerializer(customer, data=data, partial=True)

    if customer_serializer.is_valid():
        customer_serializer.save()

        return Response({
            "message": "Customer update information successfully",
            "customer": customer_serializer.data
        }, status=200)

    return Response(customer_serializer.errors, status=400)

@api_view(['DELETE'])
def deleteAccount(request):
    user_id = request.session.get('user_id') 
    if not user_id:
        return Response({'error': 'User not logged in or session expired'}, status=400)

    try:
        customer = get_object_or_404(Customer, id=user_id)  
        cart_url = f'http://localhost:8000/cart/delete_cart/{user_id}'  
        cart_response = requests.delete(cart_url)
        customer.delete()

        return Response({'message': 'Account and cart deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def getAllCustomers(request):
    user_id = request.session.get('user_id')  

    if not user_id:
        return Response({"error": "User ID not found in session."}, status=400)
    
    admin_customer = get_object_or_404(Customer, id=user_id)

    # Check if the requesting user is an admin
    if admin_customer.customer_type.name != 'admin':
        return Response({"error": "You do not have permission to view all customers."}, status=403)

    # Fetch all customers and their related address (if exists)
    customers = Customer.objects.select_related('customer_type').all()
    
    allCustomers = []

    for c in customers:
        # Handle cases where a customer may not have an address
        try:
            address_data = {
                "house_number": c.address.house_number,
                "road": c.address.road,
                "district": c.address.district,
                "city": c.address.city
            }
        except Address.DoesNotExist:
            address_data = None  # Set to None if no address exists

        customer_data = {
            "id": c.id,
            "username": c.username,
            "email": c.email,
            "phone_number": c.phone_number,
            "customer_type": c.customer_type.name,
            "address": address_data  # Assign address data (None if not found)
        }

        allCustomers.append(customer_data)

    return Response({"customers": allCustomers}, status=200)

@api_view(['PUT'])
def updateCustomerForAdmin(request, customer_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return Response({"error": "User ID not found in session."}, status=400)

    admin_user = get_object_or_404(Customer, id=user_id)

    # Check if the logged-in user is an admin
    if admin_user.customer_type.name != 'admin':
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    # Fetch the customer to be updated
    customer_to_update = get_object_or_404(Customer, id=customer_id)
    data = request.data

    # Ensure password is hashed if updated
    if 'password' in data:
        data['password'] = make_password(data['password'])

    # Update customer fields (admin can update `customer_type`)
    customer_serializer = CustomerSerializer(customer_to_update, data=data, partial=True)

    if customer_serializer.is_valid():
        customer_serializer.save()

        # Handle single address update
        if "address" in data:
            address_data = data["address"]

            if hasattr(customer_to_update, "address"):
                # Update existing address
                for key, value in address_data.items():
                    setattr(customer_to_update.address, key, value)
                customer_to_update.address.save()
            else:
                # Create a new address if it doesn't exist
                Address.objects.create(customer=customer_to_update, **address_data)

        return Response({
            "message": f"Customer {customer_id} updated successfully",
            "customer": customer_serializer.data
        }, status=200)

    return Response(customer_serializer.errors, status=400)