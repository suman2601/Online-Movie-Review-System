from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.

def home(request):
    query = request.GET.get("title")
    allMovie = None
    if query:
        allMovie = Movie.objects.filter(name__icontains=query)
    else: 
        allMovie = Movie.objects.all()
    
    context = {
        "movies": allMovie,
    }


    return render(request, 'movie/index.html', context)

def details(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=id).order_by("-comment")
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    
    
    if average == None:
        average = 0
    average = round(average, 1)
    context = {
        "movie": movie,
        "reviews": reviews,
        "average": average,
    }

    return render(request, 'movie/details.html', context)



def add_movie(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

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
        #if user is not admin
        else:
            return redirect("movie:home")
    # if user is not logged in
    #else:
    return redirect("user:login")


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


#Review

def add_review(request, id):
    if request.user.is_authenticated:
        
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("movie:details", id)

        else:
            form = ReviewForm()

        return render(request, 'movie/details.html', {"form": form})
    
    return redirect("user:login")

def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie, id=review_id)

        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Select value from 0 to 10."
                        return render(request, 'movie/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("movie:details", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'movie/editreview.html', {"form": form})
        else:
            return redirect("movie:details", movie_id)
  
    return redirect("user:login")

def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie, id=review_id)

        if request.user == review.user:
            review.delete()
        return redirect("movie:details", movie_id)
    else:        
        return redirect("user:login")             

