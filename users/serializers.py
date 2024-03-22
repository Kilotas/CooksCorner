from rest_framework import serializers
from .models import User
from dishes.models import Recipe
from dishes.serializers import RecipeSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'follow']

    def update(self, instance, validated_data):
        # получаем идентификатор пользователя на которого нужно подписаться или отписаться
        follower_user_id = validated_data.get('follow')

        # проверяем получили ли мы идентификатор
        if follower_user_id:
            # Получаем пользователя на которого нужно подписаться или отписаться
            followed_user = User.objects.get(id=follower_user_id)

            # проверка что пользователь не пытается подписаться на самого себя
            if followed_user != instance:
                # Проверяем, подписан ли пользователь на указанного пользователя
                instance.following.remove(followed_user)
            else:
                # если не подписан, то отписываемся
                instance.following.add(followed_user)

        # возвращаение обновленного объекта пользователя
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, user):
        recipes = Recipe.objects.filter(author=user)
        serializer = RecipeSerializer(recipes, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'bio', 'image', 'first_name', 'last_name', 'recipes')



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'first_name', 'last_name']


