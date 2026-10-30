from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=200, unique=True)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 8.8
    image = models.ImageField()  # jastai "inception.jpg"

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    rating = models.FloatField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)