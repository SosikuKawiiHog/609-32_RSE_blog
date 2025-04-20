from django.http import HttpResponse
from django.shortcuts import render

from articles.models import Article


def homepage(request):
    best_articles = Article.objects.order_by('-date')[:3]
    data = { "header": "Главная", "message": "ЗДАРОВА! Это сайт со всякими программными приколами.", "best_articles": best_articles }
    return render(request, 'homepage.html', context=data)

def about(request):
    header = "О нас"
    staff = [ 'Mahajran Habibivich' ]
    director = { "name": "Я", "img": '/media/images/default.jpg' }
    address = ( ' Проспект Ленина.', 'Сургут', 'SUR78', 'РФ' )
    data = { "header": header, "staff": staff, "director": director, "address": address }
    return render(request, 'about.html', data)