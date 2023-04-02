from .models import UserProfile
from rest_framework import viewsets
from rest_framework import permissions
from . permissions import IsOwnerOrReadOnly , PostUserWritePermission
from . serializers import ProfileSerializer
from users.models import NewUser

# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]   
    # permission_classes = [PostUserWritePermission ]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.NewUser)
