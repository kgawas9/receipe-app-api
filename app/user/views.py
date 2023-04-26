"""
Views for the user API.
"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# from rest_framework.response import Response
# from rest_framework import status

# from rest_framework.views import APIView

from user.serializers import (
    UserSerializzer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializzer


# class CreateUserView(APIView):
#     def post(self, request):
#         serializer = UserSerializzer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(status.HTTP_201_CREATED)
#             return Response({
#                 'status_code': status.HTTP_201_CREATED,
#                 'message': 'User succesfully created.',
#             })
#         else:
#             return Response({
#                 'status_code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'Something went wrong.',
#             })


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
