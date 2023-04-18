from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import SignupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Relation

User = get_user_model()


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    
    
class ProfileView(APIView):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # lookup_url_kwarg = 'username'
    # lookup_field = 'username'    
    # print(serializer_class['is_private'])
    # # TODO : write private pages
    
    def get(self, request, username, *args, **kwargs):
        wanted_user = User.objects.get(username=username)
        try:
            profile = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)

        serializer = UserSerializer(profile)
        if serializer['is_private'].value == True:
            try:
                follow = Relation.objects.filter(from_user=request.user, to_user=wanted_user).exists()
            except:
                return Response({"error": "This account is private and you are not following it yet"})
            
            if follow == True:     
                return Response(serializer.data)
            else:
                return Response({"error": "This account is private and you are not following it yet"})
        


class SelfProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)