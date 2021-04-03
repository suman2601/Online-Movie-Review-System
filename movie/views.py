from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
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

def watchlist_add(request, movie_id):
    item_to_save = get_object_or_404(Movie, pk=movie_id)
    # Check if the item already exists in that user watchlist
    if Watchlist.objects.filter(user=request.user, item=movie_id).exists():
        #messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("movie:home"))
    
    # Get the user watchlist or create it if it doesn't exists
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
   
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(item_to_save)
    #messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    obj = Watchlist.objects.get(user=request.user)
    watchlist= obj.item.all()
    for x in watchlist:
        print(x.name)
    return render(request, 'movie/watchlist.html', {'watchlist':watchlist})

def watchlist_del(request, movie_id):
    item_to_del = get_object_or_404(Movie, pk=movie_id)
    obj = Watchlist.objects.get(user=request.user)
    obj.item.remove(item_to_del)
    return redirect("movie:home")             

def watchlist_view(request):
    obj = Watchlist.objects.get(user=request.user)
    watchlist = obj.item.all()
    return render(request, 'movie/watchlist.html', {'watchlist':watchlist})
