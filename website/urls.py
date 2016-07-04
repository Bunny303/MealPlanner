from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^$', views.HomePageView.as_view(), name='home'),
                  url(r'^recipes/$', views.RecipeList.as_view()),
                  url(r'^grocery-list/$', views.GroceryList.as_view()),
                  url(r'^recipes/$', views.RecipeList.as_view(), name='recipe-list'),
                  url(r'^my-recipes/$', views.RecipeList.as_view(), name='my-recipe-list'),
                  url(r'^grocery-list/$', views.GroceryList.as_view(), name='grocery-list'),
                  url(r'^add-ingredient/$', views.RecipeIngredientCreate.as_view(), name='recipeingredient-create'),
                  url(r'^delete-ingredient/$', views.RecipeIngredientDelete.as_view(), name='recipeingredient-delete'),
                  url(r'^remove-grocery/$', views.RecipeIngredientUpdate.as_view(), name='recipeingredient-update'),
                  url(r'^delete-recipe/(?P<pk>[0-9]+)/(?P<next>[0-9]+)/$', views.RecipeDelete.as_view(), name='recipe-delete'),
                  url(r'^update-recipe/(?P<pk>[0-9]+)/$', views.RecipeUpdate.as_view(), name='recipe-update'),
                  url(r'^view-recipe/(?P<pk>[0-9]+)/$', views.RecipeDetailView.as_view(), name='recipe-detail'),
                  url(r'^new-recipe/$', views.RecipeCreate.as_view(), name='recipe-create'),
                  url(r'^week-menu/$', views.WeekView.as_view(), name='week'),
                  url(r'^add-meal/$', views.MealAddView.as_view(), name='meal-create'),
                  url(r'^remove-meal/$', views.MealDelete.as_view(), name='meal-delete'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, )
