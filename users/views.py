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











class usersLestView(viewsets.ModelViewSet):  
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FultDataUserSerializer   
    queryset = NewUser.objects.all()   



    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(NewUser, slug=item)

    # # Define Custom Queryset
    # def get_queryset(self):
    #     return NewUser.objects.all()


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(seFavorite_Modelslf, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













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
            
# localStorage

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


# class UserDataView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(FultDataUserSerializer(request.user).data)



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







