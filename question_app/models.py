from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class AnswerType(models.Model):
    type = models.CharField("Тип", max_length=256, blank=True, null=False)
    description = models.CharField("Описание", max_length=256, blank=True, null=False)

    class Meta:
        db_table = 'AnswerTypes'
        verbose_name = 'Тип ответа'
        verbose_name_plural = 'Типы ответов'

    def __str__(self):
        return "%s | %s " % (self.type, self.description)


class Interview(models.Model):
    interview = models.CharField("Опрос", max_length=64)
    created = models.DateTimeField("Создано", auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Обновлено", auto_now_add=False, auto_now=True)

    class Meta:
        db_table = 'interview'
        ordering = ['created']
        verbose_name = 'Опроса'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.interview


class Question(models.Model):
    question = models.TextField("Вопрос")
    user = models.ForeignKey(User, null=False, verbose_name=u'Автор', on_delete=models.CASCADE)
    answer_type = models.ForeignKey(AnswerType, verbose_name=u'Тип ответа', on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, verbose_name=u'Опрос', on_delete=models.CASCADE, blank=True, null=True,
                                  default=None)
    created = models.DateTimeField("Создано", auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Обновлено", auto_now_add=False, auto_now=True)

    class Meta:
        db_table = 'questions'
        ordering = ['created', 'interview']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return "%s " % (self.question)


class Answer(models.Model):
    answer = models.CharField("Ответ", max_length=256)
    question = models.ForeignKey(Question, null=False, verbose_name=u'Вопрос', on_delete=models.CASCADE)
    votes = models.IntegerField("Голосов", default=0)
    created = models.DateTimeField("Создано", auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Обновлено", auto_now_add=False, auto_now=True)

    class Meta:
        db_table = 'answers'
        ordering = ['question', 'created']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return "%s | %s " % (self.answer, self.votes)


class VotesResult(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField("Создано", auto_now_add=True, auto_now=False)
    update = models.DateTimeField("Обновлено", auto_now_add=False, auto_now=True)

    class Meta:
        db_table = 'Votes_Result'
        ordering = ['created', 'interview']
        verbose_name = u'Результат опроса'
        verbose_name_plural = u'Результаты опроса'

    def __str__(self):
        return "Результаты"
