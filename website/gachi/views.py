from django.shortcuts import render


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
            '한국어 - 이것은 예시입니다. 예시라고요',
            'English - This is a description for sample template. Our website will be look like this',
            'Español - Éste es el modelo de nuestra página web.',
        ]
    }
    return render(request, template_name='gachi/index.html', context=sample_context)
