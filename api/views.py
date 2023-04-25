from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import SignupSerializer, UserSerializer, FollowersSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Relation, Post
from rest_framework import status

User = get_user_model()



class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    
    
class ProfileView(APIView):
    def get(self, request, username, *args, **kwargs):
        wanted_user = User.objects.get(username=username)
        try:
            profile = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        if username ==  request.user.username:
            serializer = UserSerializer(profile)
            return Response(serializer.data)
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
        return Response(serializer.data)
    
class FollowersView(generics.ListAPIView):
    def get(self, request, username, *args, **kwargs):
        try:
            user_id = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        print(type(username))
        print(type(request.user.username))
        
        if username ==  request.user.username:
            followers = Relation.objects.filter(to_user=user_id)

            serializer = FollowersSerializer(followers, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        if user_id.is_private:
            try:
                follow = Relation.objects.filter(from_user=request.user, to_user=user_id).exists()
            except:
                return Response({"error": "This account is private and you are not following it yet"})
            
            if follow == True:     
                followers = Relation.objects.filter(to_user=user_id)

                serializer = FollowersSerializer(followers, many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response({"error": "This account is private and you are not following it yet"})
        else:
            followers = Relation.objects.filter(to_user=user_id)

            serializer = FollowersSerializer(followers, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        # Default response
        return Response({"error": "Invalid request."})



                          

class FollowingsView(generics.ListAPIView):    
    def get(self, request, username, *args, **kwargs):
        try:
            user_id = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        print(type(username))
        print(type(request.user.username))
        
        if username ==  request.user.username:
            followers = Relation.objects.filter(from_user=user_id)

            serializer = FollowersSerializer(followers, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        if user_id.is_private:
            try:
                follow = Relation.objects.filter(from_user=request.user, to_user=user_id).exists()
            except:
                return Response({"error": "This account is private and you are not following it yet"})
            
            if follow == True:     
                followers = Relation.objects.filter(from_user=user_id)

                serializer = FollowersSerializer(followers, many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response({"error": "This account is private and you are not following it yet"})
        else:
            followers = Relation.objects.filter(from_user=user_id)

            serializer = FollowersSerializer(followers, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        # Default response
        return Response({"error": "Invalid request."})
    
    
class PostRetrieveView(APIView):

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)   
        if user.is_private:
            try:
                follow = Relation.objects.filter(from_user=request.user, to_user=user).exists()
            except:
                return Response({"error": "This account is private and you are not following it yet"})

        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
     
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        print (data)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error":"bad request"},status=status.HTTP_400_BAD_REQUEST)    

class PostUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        if not instance:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['user'] = request.user.id
        serializer = PostSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    
class PostDeleteView(generics.DestroyAPIView):    
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ok":"post deleted"},status=status.HTTP_204_NO_CONTENT)
