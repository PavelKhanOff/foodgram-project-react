from django.db import models
from django.utils.html import format_html

from users.models import CustomUser


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='followers')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} => {self.author}'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    hex_color = models.CharField(max_length=7, default="#ffffff")
    slug = models.SlugField(max_length=50)

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hex_color,
        )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество/объем')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='recipes')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="static/", verbose_name="Фото блюда")
    text = models.TextField(max_length=1000)
    ingredients = models.ManyToManyField(
        Ingredient, related_name='ingredients')
    tags = models.ManyToManyField(Tag, related_name='tags')
    cooking_time = models.TimeField(
        verbose_name='Время приготовления')
    is_favorited = models.ManyToManyField(
        CustomUser,
        related_name='is_subscribed',
        verbose_name='Сохранившие'
    )
    is_in_shopping_cart = models.ManyToManyField(
        CustomUser,
        related_name='is_in_shopping_cart',
        verbose_name='В списке покупок'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='purchases', verbose_name='Пользователь')
    purchase = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='customers', verbose_name='Покупка')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Списки Покупок'


class Favorites(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="favorite_subscriber")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
