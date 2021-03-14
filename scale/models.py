"""
Models for scales
"""
from django.contrib.auth.models import User
from django.db import models

class Scale(models.Model):
    """
    Scale has a title, number of votes, possibly parent_scale it belongs to
    """
    scale_title = models.CharField(max_length=200)
    parent_scale = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    yay_or_nay_of_parent = models.CharField(max_length=4, blank=True, null=True)#Either 'yay' or 'nay'
    nays = models.IntegerField(default=0)
    yays = models.IntegerField(default=0)

    def __str__(self):
        return self.scale_title

class Votes(models.Model):
    """
    Joining table for User and Scale. User can have a vote on scale. Vote is yay or nay.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    vote = models.CharField(max_length=8, blank=True, null=True)#Either 'yay' or 'nay' or 'nothing'
