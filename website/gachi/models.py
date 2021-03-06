# -*- coding: utf-8 -*-

from django.db import models


# Create your models here.
class Proverb(models.Model):
    """
    Proverb model
    """
    category = models.CharField(max_length=10)
    text = models.CharField(max_length=200)


class Person(models.Model):
    """
    Person model
    In separate view, model is generated by getting form inputs.
    """
    selected_proverb = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return 'Model class for Person'

    def find_category(self):
        """
        Finds category of selected proverb
        :return: Category of proverb
        """
        # load all proverbs
        all_proverbs = Proverb.objects.all()
        for proverb in all_proverbs:
            if proverb.text == self.selected_proverb:
                return proverb.category


class AnalysisInfo(models.Model):
    """
    Analysis model common information
    Does not require separate database table.
    Contains category of proverb, and number of times that category was selected by users
    """
    category = models.CharField(max_length=10)
    selected_times = models.IntegerField()

    def __str__(self):
        return 'Common information of analysis model'


class AnalysisByAge(models.Model):
    """
    Analysis model - by age
    """
    age_range = models.CharField(max_length=10)
    analysis_info = models.ForeignKey(AnalysisInfo, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return 'Data analysis model of gachi - by age'


class AnalysisByGender(models.Model):
    gender = models.CharField(max_length=1)
    analysis_info = models.ForeignKey(AnalysisInfo, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return 'Data analysis model of gachi - by gender'

