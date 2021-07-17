import django_filters.rest_framework
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import RecipeFilter

from .models import (CustomUser, Favorites, Follow, Ingredient, Recipe,
                     ShoppingList, Tag)
from .permissions import IsAuthor
from .serializers import (AddFavouriteRecipeSerializer, CreateRecipeSerializer,
                          IngredientSerializer, ListRecipeSerializer,
                          ShowFollowersSerializer, TagSerializer,
                          UserSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter

    def get_permissions(self):
        if self.action == 'create':
            return IsAuthenticated(),
        if self.action in ['destroy', 'update', 'partial_update']:
            return IsAuthor(),
        return AllowAny(),

    def get_serializer_class(self):
        if self.action == 'list':
            return ListRecipeSerializer
        if self.action == 'retrieve':
            return ListRecipeSerializer
        return CreateRecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def showfollows(request):
    users = request.user.followers.all()
    user_obj = []
    for follow_obj in users:
        user_obj.append(follow_obj.author)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = ShowFollowersSerializer(
        result_page, many=True, context={'current_user': request.user})
    return paginator.get_paginated_response(serializer.data)


class FollowViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=user_id)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                'Вы уже подписаны',
                status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        serializer = UserSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        author = CustomUser.objects.get(id=user_id)
        try:
            follow = Follow.objects.get(user=user, author=author)
            follow.delete()
            return Response('Удалено',
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Подписки не было',
                            status=status.HTTP_400_BAD_REQUEST)


class FavouriteViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorites.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Вы уже добавили рецепт в избранное',
                status=status.HTTP_400_BAD_REQUEST)
        Favorites.objects.create(user=user, recipe=recipe)
        serializer = AddFavouriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            add_favourite = Favorites.objects.get(user=user, recipe=recipe)
            add_favourite.delete()
            return Response('Удалено',
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Рецепт не был в избранном',
                            status=status.HTTP_400_BAD_REQUEST)


class ShoppingListViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingList.objects.filter(user=user, purchase=recipe).exists():
            return Response(
                'Вы уже добавили рецепт в список покупок',
                status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, purchase=recipe)
        serializer = AddFavouriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            add_shopping_list = ShoppingList.objects.get(
                user=user, purchase=recipe)
            add_shopping_list.delete()
            return Response(
                'Удалено', status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                'Рецепт не был в списке покупок',
                status=status.HTTP_400_BAD_REQUEST)


class DownloadShoppingCart(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        users_shopping_list_recipes = user.purchases.all()
        recipes = []
        for i in users_shopping_list_recipes:
            recipes.append(i.purchase)
        ingredients = []
        for recipe in recipes:
            ingredients.append(recipe.ingredients.all())
        new_ingredients = []
        for set in ingredients:
            for ingredient in set:
                new_ingredients.append(ingredient)
        ingredients_dict = {}
        for ing in new_ingredients:
            if ing in ingredients_dict.keys():
                ingredients_dict[ing] += ing.quantity
            else:
                ingredients_dict[ing] = ing.quantity
        wishlist = []
        for k, v in ingredients_dict.items():
            wishlist.append(f'{k.name} - {v} {k.unit} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
