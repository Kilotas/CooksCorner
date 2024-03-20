from django.db import models
from authorization.models import User

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'
DIFFICULTY_CHOICES = [
    (EASY, 'Easy'),
    (MEDIUM, 'Medium'),
    (HARD, 'Hard'),
]

BREAKFAST = 'BREAKFAST'
LUNCH = 'LUNCH'
DINNER = 'DINNER'

CATEGORY_CHOICES = [
    (BREAKFAST, 'Breakfast'),
    (LUNCH, 'Lunch'),
    (DINNER, 'Dinner')
]

# Create your views here.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    ingredients = models.TextField(max_length=400)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTY_CHOICES, default=EASY)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    cooking_time = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    likes = models.ManyToManyField(User, through='Like', related_name='likes_recipes')
    saved_by_users = models.ManyToManyField(User, through='SavedRecipe', blank=True, related_name='saved_recipes')

    def __str__(self):
        return self.title


class Like(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('users', 'recipe') # значает, что один пользователь не может оставить более одного лайка на один и тот же рецепт.
# Create your models here.


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

