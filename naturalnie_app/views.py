from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import IngredientCheckForm, IngredientAddForm, LoginForm, AddUserForm
from .models import Ingredient, Recipe
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout


class IngredientCheck(TemplateView):
    template_name = 'ingredient_check.html'
    model = Ingredient

    def get_context_data(self, **kwargs):
        if self.request.GET:
            form = IngredientCheckForm(self.request.GET)
            if form.is_valid():
                composition2 = form.cleaned_data['composition'].replace(",", " ").replace("/", " ").replace("*", " ")
                composition_lower = composition2.lower()
                composition3 = composition_lower.split()

                data_ing1 = Ingredient.objects.values_list('name', flat=True)
                data_ing2 = Ingredient.objects.values_list('second_name', flat=True)
                data_ing3 = Ingredient.objects.values_list('third_name', flat=True)
                data_ing1list1 = list(data_ing1)
                data_ing1list2 = list(data_ing2)
                data_ing1list3 = list(data_ing3)
                data_ing_list = data_ing1list1 + data_ing1list2 + data_ing1list3

                data_ing_list_clean = filter(None, data_ing_list)

                db_ing = []
                for i in data_ing_list_clean:
                        ingredient = i.lower()
                        db_ing.append(ingredient)

                ingredients_list = []
                unknown_products = []
                for i in composition3:
                    if i in db_ing:
                        ingredients_list.append(i)
                    else:
                        unknown_products.append(i)


                ingredients_in_db = []
                for i in ingredients_list:
                    ingredient = Ingredient.objects.get(
                        Q(name__iexact=i) |
                        Q(second_name__iexact=i) |
                        Q(third_name__iexact=i)
                    )
                    ingredients_in_db.append(ingredient)

                ingredients = []
                [ingredients.append(i) for i in ingredients_in_db if i not in ingredients]

                #ingredients.append(unknown_products)


            else:
                ingredients = []
        else:
            form = IngredientCheckForm()
            ingredients = None
        ctx = {"form": form,
               "ingredients": ingredients,
               }
        return ctx


class IngredientList(TemplateView):
    template_name = 'ingredient_list.html'
    def get_context_data(self):
        return {'ingredients': Ingredient.objects.all()}

class IngredientAdd(View):
    def get(self, request):
        form = IngredientAddForm()
        return render(request, "add_ingredient.html", {"form": form})

    def post(self, request):
        form = IngredientAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            second_name = form.cleaned_data["second_name"]
            third_name = form.cleaned_data["third_name"]
            description = form.cleaned_data["description"]
            ingredient_category = form.cleaned_data["ingredient_category"]
            new_ingredient = Ingredient.objects.create(
                name=name,
                second_name=second_name,
                third_name=third_name,
                description=description,
                ingredient_category=ingredient_category,
            )
            return redirect("ingredient-list")
        return render(request, "add_ingredient.html", {"form": form})


class IngredientDelete(DeleteView):
    model = Ingredient
    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('ingredient-list'))


class RecipeList(TemplateView):
    template_name = 'recipe_list.html'
    def get_context_data(self):
        return {'recipes': Recipe.objects.all()}


class AddUser(CreateView):
    form_class = AddUserForm
    template_name = 'add_user.html'
    success_url = reverse_lazy("profile")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["login"],
                            password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("Błąd logowania")
        return redirect(reverse_lazy('ingredient-check'))


class LogoutView(View):
    def get(self, request):
       return render(request, "logout.html")
    def post(self, request):
       logout(request)
       return redirect(reverse_lazy('ingredient-check'))


# class ResetPassword(PermissionRequiredMixin, FormView):
#     permission_required = 'auth.change_user'
#
#     form_class = ResetPasswordForm
#     template_name = "reset_password.html"
#     success_url = reverse_lazy('profile')
#
#     def get_context_data(self, *args, **kwargs):
#         ctx = super().get_context_data(*args, **kwargs)
#         password_owner = get_object_or_404(User, id=self.kwargs.get('user_id'))
#         ctx.update({'password_owner': password_owner})
#         return ctx
#
#     def form_valid(self, form):
#         user_id = self.kwargs.get('user_id')
#         user = get_object_or_404(User, id=user_id)
#         user.set_password(form.cleaned_data['password_1'])
#         user.save()
#         return redirect(self.success_url)


class UserProfile(View):
    def get(self, request):
        return render(request, "user_profile.html")
