from django import forms
from .models import Ingredient, INGREDIENT_CATEGORY
from django.contrib.auth.models import User


class IngredientCheckForm(forms.Form):
    composition = forms.CharField(label=False, max_length=450, widget=forms.Textarea, strip=True)


class IngredientAddForm(forms.Form):
    name = forms.CharField(label="Nazwa:", max_length=64)
    second_name = forms.CharField(label="Druga nazwa:", max_length=64, required=False)
    third_name = forms.CharField(label="Trzecia nazwa:", max_length=64, required=False)
    description = forms.CharField(label="Opis", max_length=400)
    ingredient_category = forms.ChoiceField(choices=INGREDIENT_CATEGORY)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=64)
    password = forms.CharField(label="Hasło", max_length=64, widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)

class AddUserForm(UserForm):
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        if User.objects.filter(username=self.data['username']).exists():
            self.add_error('username', error='Użytkownik już istnieje w bazie')
        return self.data['username']

    def clean(self):
        if self.data['password_1'] != self.data['password_2']:
            self.add_error(None, error='Hasła nie pasują do siebie')
        return super().clean()

    def save(self):
        user_data = self.cleaned_data
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password_1'],
        )
        return user

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ('password_1', 'password_2')


# class ResetPasswordForm(forms.Form):
#     password_1 = forms.CharField(widget=forms.PasswordInput,
#                                  help_text="Wpisz dwa razy to samo")
#     password_2 = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self):
#         if self.data['password_1'] != self.data['password_2']:
#             raise ValidationError('Hasła nie pasują do siebie')
#         return super().clean()