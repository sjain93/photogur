from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment
from photogur.forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def root(request):
    return HttpResponseRedirect("pictures")


def pictures(request):
    context = {"pictures": Picture.objects.all()}
    response = render(request, "pictures.html", context)
    return HttpResponse(response)


def picture_show(request, id):
    picture = Picture.objects.get(pk=int(id))
    comments_pic = picture.comments.all()
    context = {"picture": picture, "pic_com": comments_pic}
    response = render(request, "picture.html", context)
    return HttpResponse(response)


def picture_search(request):
    query = request.GET["query"]
    search_results = (
        Picture.objects.filter(artist__icontains=query)
        | Picture.objects.filter(title__icontains=query)
        | Picture.objects.filter(url__icontains=query)
    )
    context = {"pictures": search_results, "query": query}
    response = render(request, "search_results.html", context)
    return HttpResponse(response)


def create_comment(request):
    picture = Picture.objects.get(pk=request.POST["picture"])
    comment = picture.comments.create(
        name=request.POST["name"], message=request.POST["comment"]
    )
    return HttpResponseRedirect("/pictures/{}".format(picture.pk))


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login Failed')
    else:
        form = LoginForm()

    context = {"form": form}
    response = render(request, "login.html", context)
    return HttpResponse(response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')
