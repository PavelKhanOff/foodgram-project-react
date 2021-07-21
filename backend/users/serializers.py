from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from api.models import Follow

from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'password', 'first_name', 'last_name'
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def check_if_is_subscribed(self, user):
        current_user = self.context['request'].user
        other_user = user.following.all()
        if other_user.count() == 0:
            return False
        if Follow.objects.filter(user=user, author=current_user).exists():
            return True
        return False
