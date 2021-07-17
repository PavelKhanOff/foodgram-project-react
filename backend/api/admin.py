from django.contrib import admin

from .models import Favorites, Follow, Ingredient, Recipe, ShoppingList, Tag

admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Favorites)
admin.site.register(ShoppingList)
