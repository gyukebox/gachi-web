# -*- coding: utf-8 -*-

import json
import numpy as np

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import *


# Create your views here.
def index(request):
    """
    Index view. Renders index.html
    URL: host/
    :param request: Http request instance
    :return: Rendered template, named index.html
    """

    sample_context = {
        'proverbs': [

        ],
        'description': [
            '함께 찾는 우리의 가치: 당신의 삶에서 가장 중요한 것은 무엇입니까?',
            '여러분들께 몇 가지의 문구를 보여 드릴 겁니다. 보시고 가장 마음에 드시는 문구 하나만 골라 주세요!'
        ]
    }

    try:
        json_file = open('/static/gachi/config.json', 'r', encoding='utf8')
        json_object = json.load(json)

        for i in range(6):
            start_index = json_object["Proverbs"][i]["Start"]
            end_index = json_object["Proverbs"][i]["End"]

            key = np.random.randint(low=start_index, high=end_index + 1)
            sample_context['proverbs'].append(Proverb.objects.get(pk=key).text)

        json_file.close()
    except FileNotFoundError:
        indices = [1, 10, 20, 27, 38, 47, 55]
        for i in range(6):
            start_index = indices[i]
            end_index = indices[i + 1]

            key = np.random.randint(low=start_index, high=end_index + 1)
            sample_context['proverbs'].append(Proverb.objects.get(pk=key).text)

    return render(request, template_name='gachi/index.html', context=sample_context)


def get_person_answer(request):
    """
    View function for receiving form input.
    URL: host/submit
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            # parse form
            query_string = request.body.decode('utf-8')
            params = query_string.split('\r\n')
            print(params)

            # parse actual values
            proverb = params[0][(params[0].index('=')) + 1:]
            age = params[1][(params[1].index('=')) + 1:]
            gender = params[2][(params[2].index('=')) + 1:]

            # generate model and insert into DB
            person = Person(selected_proverb=proverb, age=int(age), gender=gender)
            person.save()

            # TODO implementation of result template
            return HttpResponseRedirect('/analysis')
        except ValueError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def analyze(request):
    """
    View function for analyzing data
    URL: host/analysis
    :param request:
    :return:
    """
    people = Person.objects.all()
    people = sorted(people, key=lambda x: x.age)

    # test
    for person in people:
        print('=' * 50)
        print(person.find_category())
        print(person.age)
        print(person.gender)

    # make analysis result into json-like dict
    analysis_result = dict()

    # TODO analysis by age
    # TODO analysis by gender

    return render(request, template_name='gachi/result.html', context=analysis_result)


def analyze_by_age(data):
    pass


def analyze_by_gender(data):
    pass
