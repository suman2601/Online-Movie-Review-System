from django.db import models

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
    
   # def __unicode__(self):
       # return self.name