"""Naturalnie_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from naturalnie_app.views import IngredientCheck, IngredientList, IngredientAdd, IngredientDelete, \
    RecipeList, LoginView, AddUser, UserProfile, LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IngredientCheck.as_view(), name="ingredient-check"),
    path('skladniki/', IngredientList.as_view(), name="ingredient-list"),
    path('dodaj_skladnik/', IngredientAdd.as_view(), name="ingredient-add"),
    path('usun_skladnik/', IngredientDelete.as_view(), name="ingredient-delete"),
    path('przepisy/', RecipeList.as_view(), name="recipe-list"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', AddUser.as_view(), name="register"),
    path('profil/', UserProfile.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)