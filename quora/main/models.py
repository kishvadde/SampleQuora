from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):

    text = models.TextField(unique=True)
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asked_on = models.DateTimeField()
    votes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.text

class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)
    answered_on = models.DateTimeField()
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('question', 'answered_by')

    def __str__(self):
        return self.text


class QuestionVote(models.Model):

    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.question.text + '-' + self.voted_by.username

    class Meta:
        unique_together = ('question','voted_by')


class AnswerVote(models.Model):

    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.text + '-' + self.voted_by.username

    class Meta:
        unique_together = ('answer','voted_by')

