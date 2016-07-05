from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    UNITS = (
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        (None, None),
        ('tbsp', 'tbsp'),
    )
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=6, choices=UNITS, default='kg', blank=True, null=True)

    # price = models.FloatField(default=0.0)

    def __str__(self):
        return "{}, {}".format(self.name, self.unit)


class Recipe(models.Model):
    CATEGORIES = (
        (1, 'Main Dish'),
        (2, 'Salad'),
        (3, 'Soup'),
        (4, 'Desert'),
    )

    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=550, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    image = models.ImageField(null=True, upload_to="static")
    portion_number = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.IntegerField(choices=CATEGORIES, default=None, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe, default=None, blank=True, null=True)
    quantity = models.FloatField(default=1.0)
    forShopping = models.BooleanField(default=True)

    def __str__(self):
        return "{}{} {}".format(self.quantity, self.ingredient.unit, self.ingredient.name)


class Day(models.Model):
    DAYS = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    )
    # todo: make name unique
    name = models.CharField(max_length=3, choices=DAYS)
    recipe = models.ManyToManyField(Recipe, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
