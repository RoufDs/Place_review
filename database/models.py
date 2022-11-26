from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import datetime
from django.utils import timezone


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    imageUrl = models.URLField()
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def no_of_ratings(self):
        rating = Rating.objects.filter(place=self)
        return len(rating)
    
    def avg_ratings(self):
        rating = Rating.objects.filter(place=self)
        sum = 0
        for r in rating:
            sum += r.stars
        if len(rating) > 0:
            return sum / len(rating)
        else:
            return 0
    
    def get_date(self):
        time = timezone.now()
        if self.created.hour == time.hour:
            return str(time.minute - self.created.minute) + " minutes ago"
        elif self.created.day == time.day:
            return str(time.hour - self.created.hour) + " hours ago"
        elif self.created.month == time.month:
            return str(time.day - self.created.day) + " days ago"
        elif self.created.year == time.year:
            return str(time.month - self.created.month) + " months ago"
        # else:
        #     return str(time.year - self.created.year) + " years ago"        
    
    def __str__(self):
        return str(self.active) + " | " + str(self.user.username) + " | "  + self.title


class Rating(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + ' | ' + self.place.title + ' | ' + str(self.stars)