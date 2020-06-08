from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys
from .s_lib import scale
from .cnn import model
from random import choice
import json

from .models import Category, Similar

def main_page(request):
    c = choice(model.CATEGORIES)
    context = {'to_draw':c}
    return render(request,'main_page.html',context)

def picture(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        body = body.split(',')
        pic = scale.prepare_image(body[1])
        response = model.predict(pic)
        return JsonResponse({'result': str(response) }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")
    else:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

def categories(request):
    categories = [category.name for category in Category.objects.all()]
    return JsonResponse({'categories': categories }, status=200)
    
def random_similar(request, category_name):
    similars = [similar for similar in Similar.objects.filter(similar_cat_name=category_name)]
    random_sim = choice(similars)
    try:
        similar_img = model.get_single_image_from_npy(random_sim.correct_cat_name, random_sim.npy_id)
        return JsonResponse({'similar': similar_img }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")
    else:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

def about(request):
    return render(request,'about.html')