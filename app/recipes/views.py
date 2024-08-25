"""
Views from the recipe APIs
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipes import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes in the database.
    List recipes, create recipes, retrieve recipes.
    """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve recipes for authenticated user.
        Override the get_queryset method to filter
        recipes by authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
        Return the serializer class for request.
        If the action is list, return RecipeSerializer,
        else return RecipeDetailSerializer
        """
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        Override the perform_create method to set
        the user field to the authenticated user.
        """
        serializer.save(user= self.request.user)

class TagViewSet(mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    Manage tags in the database.
    List tags, update tags, delete tags.
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to authenticated user.
        Override the get_queryset method to filter
        tags by authenticated user.
        """
        # return the queryset filtered by the authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-name')
