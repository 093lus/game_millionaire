from django.contrib.auth.models import User
from django.db import models
from random import randint
from django.db.models import Max
from django.core.validators import MaxValueValidator, MinValueValidator


class UserBestScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    score = models.SmallIntegerField(validators=[MaxValueValidator(20), MinValueValidator(5)])

    def __str__(self):
        return self.question_text


class RandomQuestions(Question):
    class Meta:
        proxy = True

    @classmethod
    def get_random(cls):
        count = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
        random_id = randint(1, count - 1)
        x = Question.objects.get(id=random_id)
        return x


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, )
    answer_text = models.CharField(max_length=200)
    is_answer = models.BooleanField()

    def __str__(self):
        return str(self.question)
