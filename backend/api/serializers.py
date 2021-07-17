from rest_framework import serializers

from .models import CustomUser, Follow, Ingredient, Recipe, Tag

BASE_URL = 'http://127.0.0.1'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'purchases')


class AddFavouriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingListRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ListRecipeUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def check_if_is_subscribed(self, user):
        current_user = self.context['request'].user
        other_user = user.following.all()
        if len(other_user) == 0:
            return 0
        if current_user.id in [i.user.id for i in other_user]:
            return 1
        return 0


class ListRecipeSerializer(serializers.ModelSerializer):
    author = ListRecipeUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField('check_if_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'check_if_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = '__all__'

    def check_if_is_favorited(self, recipe):
        request_data = self.context['request']
        user = request_data.user
        if user.is_anonymous:
            return 0
        user_recipes_favourited = user.favorite_subscriber.all()
        if recipe in [i.recipe for i in user_recipes_favourited]:
            return 1
        return 0

    def check_if_is_in_shopping_cart(self, recipe):
        request_data = self.context['request']
        user = request_data.user
        if user.is_anonymous:
            return 0
        user_recipes_in_shopping_cart = user.purchases.all()
        if recipe in [i.purchase for i in user_recipes_in_shopping_cart]:
            return 1
        return 0


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    author = ListRecipeUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class ShowFollowerRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowersSerializer(serializers.ModelSerializer):

    recipes = ShowFollowerRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField('count_author_recipes')
    is_subscribed = serializers.SerializerMethodField('check_if_subscribed')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def count_author_recipes(self, user):
        recipes_count = len(user.recipes.all())
        return recipes_count

    def check_if_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return 0
        if len(other_user) == 0:
            return 0
        if current_user.id in [i.user.id for i in other_user]:
            return 1
        return 0


class ShowIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    ingredients = ShowFollowerRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        exclude = ('id', 'is_favorited', 'is_in_shopping_cart', 'author')
