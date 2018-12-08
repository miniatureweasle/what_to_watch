from django.db import models

class Movie(models.Model):
    """
    Defines a user rated Movie.
    """
    title = models.TextField(blank=False, db_index=True)
    rating = models.FloatField(null=True)
    release_year = models.IntegerField(null=True)
    genre = models.TextField(null=True, blank=True)
    votes = models.IntegerField(null=True)
