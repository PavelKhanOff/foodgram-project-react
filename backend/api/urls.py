from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from .views import (DownloadShoppingCart, FavouriteViewSet, FollowViewSet,
                    IngredientViewSet, RecipesViewSet, ShoppingListViewSet,
                    TagViewSet, showfollows)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/subscriptions/', showfollows),
    path('users/<user_id>/subscribe/', FollowViewSet.as_view()),
    path('recipes/<recipe_id>/favorite/', FavouriteViewSet.as_view()),
    path('recipes/<recipe_id>/shopping_cart/', ShoppingListViewSet.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls))
]
