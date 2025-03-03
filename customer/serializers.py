from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Customer, Address, CustomerType

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['house_number', 'road', 'district', 'city']

class CustomerTypeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomerType
        fields = ['name']

class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    customer_type = serializers.SlugRelatedField(
        queryset=CustomerType.objects.all(),
        slug_field='name',
        required=False
    ) ## de hien thi customer_type la dang regular,.. thay vi hien thi id

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'customer_type' , 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def to_internal_value(self, data):
        allowed_fields = set(self.fields.keys())  # Get all valid fields
        unknown_fields = set(data.keys()) - allowed_fields  # Find invalid fields

        if unknown_fields:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in unknown_fields}
            )

        return super().to_internal_value(data)

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        validated_data['password'] = make_password(validated_data['password'])

        if 'customer_type' not in validated_data:
            validated_data['customer_type'] = CustomerType.objects.get(name='regular')

        customer = Customer.objects.create(**validated_data)

        if address_data:
            Address.objects.create(customer=customer, **address_data)

        return customer
    
    def update(self, instance, validated_data):
        """
        Custom update method to handle nested address updates.
        """
        # Handle address separately
        address_data = validated_data.pop('address', None)

        # Update customer fields
        for key, value in validated_data.items():
            if key == 'password':  # Ensure password is hashed
                setattr(instance, key, make_password(value))
            else:
                setattr(instance, key, value)

        instance.save()

        # Handle address update
        if address_data:
            if hasattr(instance, "address"):  # Update existing address
                for key, value in address_data.items():
                    setattr(instance.address, key, value)
                instance.address.save()
            else:  # Create a new address if none exists
                Address.objects.create(customer=instance, **address_data)

        return instance

