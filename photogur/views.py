from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment

def root(request):
    return HttpResponseRedirect('pictures')

# def home(request):
#     return HttpResponseRedirect('pictures')

def pictures(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk= int(id))
    comments_pic = picture.comments.all()
    context = {'picture':picture, 'pic_com':comments_pic}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)
