from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Knot(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField()
    pic = models.ImageField()
    type = models.CharField(max_length=30)
    category = models.ForeignKey(Categories, related_name='category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Knot"
        verbose_name_plural = "Knots"


class KnotInCategory(models.Model):

    knot = models.ForeignKey(Knot, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Knot - Categories relation"


class Favorite(models.Model):

    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_knot = models.ForeignKey(Knot, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorite"
