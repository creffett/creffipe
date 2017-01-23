from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Recipe
# Create your views here.


def index(request):
    recipe_list = Recipe.objects.order_by('name')
    template = loader.get_template('reffipe/index.html')
    context = {
        'recipe_list': recipe_list,
    }
    return HttpResponse(template.render(context, request))


def recipe(request, recipe_id):
    return HttpResponse("You're looking at recipe %s." % recipe_id)
