from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model


User = get_user_model()



class SignupSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'access_token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

    def get_access_token(self, obj):
        # Generate a new token for the user.
        token_data = TokenObtainPairSerializer().get_token(obj)
        return str(token_data.access_token)        
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'bio', 'website', 'is_private', 'is_verified')    