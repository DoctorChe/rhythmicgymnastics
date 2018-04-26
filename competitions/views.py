from django.shortcuts import render


def index(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'basic.html',
                  {'content':
                        ['Все свои пожелания Вы можете отправлять на наш почтовый адрес:',
                         'cool.rhythmicgymnastics@yandex.ru']
                   })
