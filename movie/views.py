from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def home(request):
    allMovie = Movie.objects.all()
    context = {
        "movies": allMovie,
    }


    return render(request, 'movie/index.html', context)

def details(request, id):
    movie = Movie.objects.get(id=id)

    context = {
        "movie": movie,
    }

    return render(request, 'movie/details.html', context)



def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        #check for if forms is valid
        if form.is_valid():
            data = form.save(commit = False)
            data.save()
            return redirect("movie:home")

    else:
        form = MovieForm()
    return render(request, 'movie/addmovies.html', {"form": form, "controller": "Add Movies"})

def update_movie(request, id):
    
    movie = Movie.objects.get(id=id)

    #form check
    if request.method == "POST":
        form = MovieForm(request.POST or None, instance=movie)

        #check for if forms is valid
        if form.is_valid():
            data = form.save(commit = False)
            data.save()
            return redirect("movie:details", id)
    
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie/addmovies.html', {"form": form,  "controller": "Update Movies"})


def delete_movie(request, id):
    
    movie = Movie.objects.get(id=id)

    #delete movie
    movie.delete()
    return redirect("movie:home")