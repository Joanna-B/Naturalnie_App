from django.contrib import admin
from .models import Ingredient, INGREDIENT_CATEGORY, Recipe


admin.site.register(Ingredient)
admin.site.register(Recipe)