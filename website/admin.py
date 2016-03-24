from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Day


# class TaskAdmin(admin.ModelAdmin):
#     list_display = [
#         'content',
#         'date',
#         'isDone',
#     ]
#     list_filter = ('isDone',)
#
# admin.site.register(Task, TaskAdmin)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Day)
