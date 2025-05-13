from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from articles import forms
from articles.models import Article


# Create your views here.
def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'articles/article_list.html', {'articles': articles})

def article_item(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_item.html', {'article': article})

@login_required(login_url='accounts:login')
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('homepage')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_form.html', {'form': form})

@login_required(login_url='accounts:login')
def article_update(request, slug):
    article = Article.objects.get(slug=slug)
    if request.user.id == article.author.id:
        if request.method == 'POST':
            form = forms.ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect('articles:article_detail', slug=slug)
        else:
            form = forms.ArticleForm(instance=article)
        return render(request, 'articles/article_form.html', {'form': form})
    return HttpResponse('401 unauthorized', status=401)

@login_required(login_url='accounts:login')
def article_delete(request, slug):
    article = Article.objects.get(slug=slug)
    if request.user.id == article.author.id:
        if request.method == 'POST':
            article.delete()
            return redirect('homepage')
        return render(request, 'articles/article_confirm_delete.html', {'article': article})
    return HttpResponse('401 unauthorized', status=401)

