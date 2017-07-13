from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, TemplateView, DetailView, UpdateView, DeleteView, FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Recipe, Ingredient, RecipeIngredient, Day
from .forms import AddRecipeForm, AddMealForm

from mixins.mixins import OwnerMixin


class HomePageView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['active'] = 'home'
        return context

class RecipeList(ListView):
    model = Recipe
    template_name = 'website/recipes.html'
    context_object_name = 'recipes'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RecipeList, self).get_context_data(**kwargs)
        url = self.request.path_info
        if url == reverse('recipe-list'):
            recipe_list = Recipe.objects.exclude(name__isnull=True).exclude(name__exact='')
        else:  # should be equal to 'my-recipe-list'
            recipe_list = Recipe.objects.filter(user=self.request.user)

        paginator = Paginator(recipe_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            recipes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            recipes = paginator.page(paginator.num_pages)

        context['recipes'] = recipes
        if url == reverse('recipe-list'):
            context['active'] = 'recipe-list'
        else:  # should be equal to 'my-recipe-list'
            context['active'] = 'my-recipe-list'

        return context


class GroceryList(LoginRequiredMixin, ListView):
    model = Day
    template_name = 'website/grocery-list.html'
    context_object_name = 'groceries'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GroceryList, self).get_context_data(**kwargs)

        groceries = {}
        for day in Day.objects.all():
            for recipe in day.recipe.all():
                for ingredient in recipe.recipeingredient_set.all():
                    if ingredient.forShopping:
                        if ingredient.ingredient in groceries:
                            groceries[ingredient.ingredient] = groceries[ingredient.ingredient] + ingredient.quantity
                        else:
                            groceries[ingredient.ingredient] = ingredient.quantity

        context['groceries'] = groceries
        context['active'] = 'grocery-list'
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'website/view-recipe.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        context['range'] = range(1, 11)
        return context


class RecipeCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipe = Recipe.objects.create(portion_number=1, user=request.user)
        return HttpResponseRedirect(reverse_lazy('recipe-update', kwargs={'pk': recipe.pk}))


class RecipeIngredientCreate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #todo : use cleaned data
        ingredient_unit = request.POST.get('ingredient_unit')
        quantity = request.POST.get('ingredient_quantity')
        ingredient_name = request.POST.get('ingredient_name')
        recipe = Recipe.objects.get(pk=request.POST.get('recipe_id'))

        try:
            ingredient = Ingredient.objects.get(name=ingredient_name.lower(), unit=ingredient_unit)
        except Ingredient.DoesNotExist:
            ingredient = Ingredient.objects.create(name=ingredient_name, unit=ingredient_unit)

        recipe_ingredient = RecipeIngredient.objects.create(quantity=quantity, ingredient=ingredient, recipe=recipe)
        # todo: extract this code in mixin
        if self.request.is_ajax():
            data = {
                'pk': recipe_ingredient.pk,
            }
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'base.html')


class RecipeIngredientDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe_ingredient = RecipeIngredient.objects.get(pk=int(request.POST.get('recipe_ingredient_id')))
        recipe_ingredient.delete()
        # todo: extract this code in mixin
        if self.request.is_ajax():
            data = {
                'success': 1
            }
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'base.html')

class RecipeIngredientUpdate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe_ingredient = RecipeIngredient.objects.get(pk=int(request.POST.get('recipe_ingredient_id')))
        # todo: find better way to do this
        recipe_ingredient.forShopping = False
        recipe_ingredient.save()
        # todo: extract this code in mixin
        if self.request.is_ajax():
            data = {
                'success': 1
            }
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'base.html')

class RecipeUpdate(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'website/modify-recipe.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('my-recipe-list')

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdate, self).get_context_data(**kwargs)
        context['range'] = range(1, 11)
        return context


class RecipeDelete(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Recipe

    def get_success_url(self):
        return '/my-recipes/' + '?page=' + self.kwargs['next']


class WeekView(LoginRequiredMixin, ListView):
    model = Day
    template_name = 'website/week.html'
    context_object_name = 'days'

    def get_context_data(self, **kwargs):
        context = super(WeekView, self).get_context_data(**kwargs)
        context['active'] = 'week'
        context['day_names'] = Day._meta.get_field('name').choices
        context['recipes'] = Recipe.objects.exclude(name__isnull=True).exclude(name__exact='')
        return context


class MealAddView(LoginRequiredMixin, FormView):
    template_name = 'week.html'
    form_class = AddMealForm
    success_url = reverse_lazy('week')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        try:
            day = Day.objects.get(name=form.cleaned_data['name'])
            for recipe in form.cleaned_data['recipe']:
                day.recipe.add(recipe)
        except Day.DoesNotExist:
            # we have no object
            # save all
            form.save()
        return super(MealAddView, self).form_valid(form)


class MealDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(pk=int(request.POST.get('recipe_id')))
        day = Day.objects.get(name=request.POST.get('day_name'))
        # todo: check what will happen if recipe id is invalid or current day is not related with found recipe
        day.recipe.remove(recipe)
        # todo: extract this code in mixin
        if self.request.is_ajax():
            data = {
                'success': 1
            }
            return JsonResponse(data, safe=False)
        else:
            return render(request, 'base.html')
