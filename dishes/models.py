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
SNACK = 'SNACK'

CATEGORY_CHOICES = [
    (BREAKFAST, 'Breakfast'),
    (LUNCH, 'Lunch'),
    (DINNER, 'Dinner'),
    (SNACK, 'Snack'),
]

# Create your views here.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    ingredients = models.TextField(max_length=400)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTY_CHOICES, default=EASY)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    cooking_time = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
# Create your models here.



