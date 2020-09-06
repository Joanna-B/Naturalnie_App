from django.db import models


INGREDIENT_CATEGORY = (
    (1, "naturalny"),
    (2, "syntetyczny"),
)

class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64, null=True)
    third_name = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=400)
    ingredient_category = models.IntegerField(choices=INGREDIENT_CATEGORY)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    picture = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=128)
    ingredients = models.CharField(max_length=256)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
