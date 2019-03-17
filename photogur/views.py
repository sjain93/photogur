from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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

@login_required
def create_comment(request):
    picture = Picture.objects.get(pk=request.POST["picture"])
    comment = picture.comments.create(
        name=request.POST["name"], message=request.POST["comment"]
    )
    return HttpResponseRedirect("/pictures/{}".format(picture.pk))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
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

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')

    else:
        form = UserCreationForm()
    response = render(request, "signup.html", {'form':form})
    return HttpResponse(response)

@login_required
def add_pic(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            add_picture = form.instance
            add_picture.user = request.user
            form.save()
            return HttpResponseRedirect('/pictures/{}'.format(add_picture.id))
    else:
        form = PictureForm()
        context = {'form': form}
        return render(request, 'add_pic.html', context)

@login_required
def edit_pic(request, id):
    picture= get_object_or_404(Picture, pk=id, user=request.user.pk)
    if request.method == 'GET':
        form = PictureForm(instance=picture)
        context = {'form':form, 'picture':picture}
        return render(request, 'edit_pic.html', context)
    elif request.method == 'POST':
        form = PictureForm(request.POST, instance=picture)
        if form.is_valid():
            edited_pic = form.save()
            return HttpResponseRedirect('/pictures/{}'.format(picture.id))
        else:
            context = {'form':form, 'picture':picture}
            response = render(request, 'edit_pic.html', context)
            HttpResponse(response)
