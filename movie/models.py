from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=300)
    director = models.CharField(max_length=50)
    cast = models.CharField(max_length=1000)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=100,null=True)
    rel_date = models.DateField()
    avg_rating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length=10000)
    rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Movie)
    
    def __str__(self):
        return f"{self.user}'s WatchList"