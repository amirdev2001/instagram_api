from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import SignupSerializer, UserSerializer, FollowersSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Relation

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
        # try:
        #     user_id = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return Response({'error': 'Profile not found'}, status=404)
        # if user_id.is_private:
        #     try:
        #         follow = Relation.objects.filter(from_user=request.user, to_user=user_id).exists()
        #     except:
        #         return Response({"error": "This account is private and you are not following it yet"})
            
        #     if follow == True:     
        #         followers = Relation.objects.filter(to_user=user_id)

        #         serializer = FollowersSerializer(followers, many=True)
        #         return Response(serializer.data)
        #     else:
        #         return Response({"error": "This account is private and you are not following it yet"})
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



                          
# class FollowingsView(generics.ListAPIView):    
#     def get(self, request, username, *args, **kwargs):
#         print(username)
#         print(request.user)
#         if username is request.user:
#             serializer = FollowersSerializer(followers, many=True)
#             print(serializer.data)
#             return Response(serializer.data)

        
#         try:
#             user_id = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({'error': 'Profile not found'}, status=404)
        
        
#         if username == request.user:
#             followers = Relation.objects.filter(from_user=user_id)

#             serializer = FollowersSerializer(followers, many=True)
#             print(serializer.data)
#             return Response(serializer.data)

        
        
#         if user_id.is_private:
#             try:
#                 follow = Relation.objects.filter(from_user=request.user, to_user=user_id).exists()
#             except:
#                 return Response({"error": "This account is private and you are not following it yet"})
            
#             if follow == True:     
#                 followers = Relation.objects.filter(from_user=user_id)

#                 serializer = FollowersSerializer(followers, many=True)
#                 print(serializer.data)
#                 return Response(serializer.data)
#         else:
#                 followers = Relation.objects.filter(from_user=user_id)

#                 serializer = FollowersSerializer(followers, many=True)
#                 print(serializer.data)
#                 return Response(serializer.data)



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