# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Person


# Create your views here.
def index(request):
    sample_context = {
        'proverbs': [
            '이것은 명언 1. 시간에 관한 명언',
            '이것은 명언 2. 성공에 관한 명언',
            '이것은 명언 3. 부에 관한 명언',
            '이것은 명언 4. 사랑에 관한 명언',
            '이것은 명언 5. 친구에 관한 명언',
            '이것은 명언 6. 배움에 관한 명언'
        ],
        'description': [
            '한국어 - 이것은 예시입니다. 예시라고요. 예시란 말이다 이사람들아 어떤 일반적 진술에 대해서 '
            '그에 관련된 특수한 진술을 미리 들어 보이는 것. 예를 들어 "감정에 대한 이해는 나이가 들수록 복잡해진다. '
            '예를 들어 시원섭섭함이라는 특수한 감정은 어느 정도 성인이 되어서야 실감할 수 있다." '
            '와 같은 방식의 서술기법을 활용하는 것이다.',
            'English - This is a description for sample template. Our website will be look like this. '
            'one of a number of things, or a part of something, taken to show the character of the whole:',
            'Español - Éste es el modelo de nuestra página web. '
            'Un ejemplo sirve para explicar o ilustrar una afirmación general, '
            'o para proporcionar un caso particular que hace de modelo para el caso general. '
            'El ejemplo es escogido libremente, pero busca aclarar la comprensión de un fenómeno o proceso dado.',
        ]
    }
    return render(request, template_name='gachi/index.html', context=sample_context)


def get_person_answer(request):
    if request.method == 'POST':
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

        return HttpResponse(params)
    else:
        return HttpResponseRedirect('/')

