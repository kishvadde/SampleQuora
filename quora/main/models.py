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

    def increment_vote(self,user):
        qv, created = QuestionVote.objects.get_or_create(question=self, voted_by=user)
        if created:
            self.votes += 1
            self.save()

    def decrement_vote(self,user):
        try:
            qv = QuestionVote.objects.get(question=self, voted_by=user)
            qv.delete()
            if self.votes > 0:
                self.votes -= 1
                self.save()
        except QuestionVote.DoesNotExist as e:
            print(e.__str__())

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


    def increment_vote(self,user):
        ans, created = AnswerVote.objects.get_or_create(answer=self, voted_by=user)
        if created:
            self.votes += 1
            self.save()

    def decrement_vote(self,user):
        try:
            ans = AnswerVote.objects.get(answer=self, voted_by=user)
            ans.delete()
            if self.votes > 0:
                self.votes -= 1
                self.save()
        except AnswerVote.DoesNotExist as e:
            print(e.__str__())


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

