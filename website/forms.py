from django import forms
from .models import Recipe, Day

DAYS = (
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday'),
)


class AddRecipeForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    portion_number = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Recipe
        exclude = ['ingredients', 'user']


class AddMealForm(forms.ModelForm):
    # recipe = forms.ModelMultipleChoiceField(queryset=[(doc.pk, doc.name) for doc in Recipe.objects.all()])
    name = forms.ChoiceField(choices=DAYS)

    class Meta:
        model = Day
        fields = ('name', 'recipe',)
