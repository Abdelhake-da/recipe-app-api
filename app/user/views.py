'''
User API views
'''

from rest_framework import generics


from user.serializes import UserSerializer


class CreateUserView(generics.CreateAPIView):
    '''Create a new user in the system'''
    serializer_class = UserSerializer

