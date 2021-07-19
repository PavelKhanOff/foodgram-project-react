from django.contrib import admin

from .models import Favorites, Follow, Ingredient, Recipe, ShoppingList, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )


admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites)
admin.site.register(ShoppingList)
