from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):

    text = models.TextField()
    asked_by = models.ManyToManyField(User)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()


class Answer(models.Model):

    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User,on_delete=models.CASCADE)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
