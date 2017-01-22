from django.db import models

# Create your models here.

MEASUREMENT = (
    ('c', 'cups'),
    ('tsp', 'teaspoons'),
    ('tbsp', 'tablespoons'),
    ('item', 'item'),
)

class Step(models.Model):
    """A step in a recipe"""
    order = models.IntegerField()
    directions = models.TextField()
    recipe = models.ForeignKey('Recipe')

class Tag(models.Model):
    """A tag to identify a recipe"""
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField('Recipe')
    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('Ingredient')
    recipe = models.ForeignKey('Recipe')
    quantity = models.FloatField()
    unit = models.CharField(choices=MEASUREMENT, max_length=10)
    description = models.CharField(max_length=100)
    notes = models.TextField()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
