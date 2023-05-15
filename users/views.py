from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import CustomUserSerializer , FultDataUserSerializer , FollowSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework import viewsets, filters, generics, permissions 
from .models import *                 
import jwt , datetime

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers



class usersLestView(viewsets.ModelViewSet):  
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FultDataUserSerializer   
    queryset = NewUser.objects.all()   



class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        try:
            serializer = CustomUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            error_list = []
            for field, errors in e.detail.items():
                for error in errors:
                    error_list.append(f"{field}: {error}")
            return Response({'errors': error_list}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = NewUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found !")
        
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password!")
        
        payload ={
            "id" : user.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat":datetime.datetime.utcnow()
        }
        
        # token = jwt.encode(payload , 'secret' , algorithm = 'HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
            'jwt': token , 
        }
        
        return response
            

class userView(APIView):
    def post(self, request):
        # token = request.post('jwt')
        token = request.data['jwt']
        print(request)
        if not token :
            raise AuthenticationFailed("Unauthenticated1!")
        
        try:
            # payload =jwt.decode(token , 'secret' , algorithm= ['HS256'])
            payload =jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = NewUser.objects.filter(id=payload['id']).first()
        serializer = FultDataUserSerializer(user)
        return Response(serializer.data)



class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data ={
            'massage': 'success'
        }
        return response














class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# Favorite Create View
class FollowCreateView(viewsets.ModelViewSet):  
    serializer_class = FollowSerializer   
    queryset = Follow_Models.objects.all() 










from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import NewUser


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': FultDataUserSerializer(user).data
            })
        else:
            return Response({'error': 'Invalid credentials'})




from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = FultDataUserSerializer(request.user)
            data = serializer.data
        except Exception as e:
            raise APIException(str(e))

        return Response(data, status=status.HTTP_200_OK)







