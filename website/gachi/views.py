# -*- coding: utf-8 -*-

from collections import Counter
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

    import json
    import numpy as np

    sample_context = {
        'proverbs': [

        ],
        'description': [
            '여러분들께 몇 가지의 문구를 보여 드릴 겁니다. 보시고 가장 마음에 드시는 문구 하나만 골라 주세요!'
        ]
    }

    try:
        json_file = open('gachi/static/gachi/config.json', 'r', encoding='utf8')
        json_object = json.load(json_file)

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

            key = np.random.randint(low=start_index, high=end_index)
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
    :param request: Http request
    :return: Template rendered, by name - result.html
    """
    people = Person.objects.all()
    people = sorted(people, key=lambda x: x.age)

    generate_worldloud([person.selected_proverb for person in people])

    data = [
        {
            'category': person.find_category(),
            'age': person.age,
            'gender': person.gender
        }
        for person in people
    ]

    # make analysis result into json-like dict
    analysis_result = dict()
    analysis_result['age'] = analyze_by_age(data)
    analysis_result['gender'] = analyze_by_gender(data)

    analysis_result['description'] = [
        '소중한 시간을 내어 주셔서 설문조사에 응해 주셔서 감사합니다!',
        '여러분들의 응답을 연령별, 그리고 성별별로 분석해 보았습니다. 확인해보시죠!'
    ]

    return render(request, template_name='gachi/result.html', context=analysis_result)


def analyze_by_age(data):
    """
    Sub-function for analysis view.
    Analyzes data by age.
    :param data: Data to analyze
    :return: Analysis, by json format
    """
    pre = [datum['category'] for datum in data if datum['age'] < 23]
    mid = [datum['category'] for datum in data if 23 <= datum['age'] < 27]
    post = [datum['category'] for datum in data if datum['age'] >= 27]

    pre_counter = Counter(pre)
    mid_counter = Counter(mid)
    post_counter = Counter(post)

    final_data = {
        'pre': sorted(pre_counter.items(), key=lambda x: x[1], reverse=True),
        'mid': sorted(mid_counter.items(), key=lambda x: x[1], reverse=True),
        'post': sorted(post_counter.items(), key=lambda x: x[1], reverse=True),
    }
    return final_data


def analyze_by_gender(data):
    """
    Sub-function for analysis view.
    Analyzes data by gender.
    :param data: Data to analyze
    :return: Analysis, by json format
    """
    male = []
    female = []
    for person in data:
        if person['gender'] == 'M':
            male.append(person)
        else:
            female.append(person)

    male_counter = Counter([data['category'] for data in male])
    female_counter = Counter([data['category'] for data in female])

    final_data = {
        'male': sorted(male_counter.items(), key=lambda x: x[1], reverse=True),
        'female': sorted(female_counter.items(), key=lambda x: x[1], reverse=True),
    }
    return final_data


def generate_worldloud(text):
    from wordcloud import WordCloud
    from konlpy.tag import Mecab

    print(text)
    phrases = ''
    for phrase in text:
        phrases += phrase + ' '

    mecab = Mecab()
    nouns = mecab.nouns(phrases)
    words = ''
    for word in nouns:
        words += word + ' '

    wordcloud = WordCloud(font_path='/Library/fonts/AppleGothic.ttf', background_color='white', width=600, height=400)
    wordcloud.generate_from_text(words)
    wordcloud.to_file('gachi/static/gachi/images/wordcloud.png')

