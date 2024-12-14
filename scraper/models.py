from django.db import models

class Product(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    rating = models.CharField(max_length=50, default='No rating')
    price = models.CharField(max_length=20, default='NA')

    def __str__(self):
        return self.title
