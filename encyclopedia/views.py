from email import utils
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from markdown2 import Markdown
from random import choice

from . import util

def index(request):
    if request.method == "POST":

        query = request.POST['q']
        #breakpoint()

        if query in util.list_entries():
            # Get the article in markdown
            article_md = util.get_entry(query)

            # Convert it to html format using markdown2
            markdowner = Markdown()
            article_html = markdowner.convert(article_md)

            return redirect(f"/{query}")

        else:
            list_articles = []
            for article in util.list_entries():
                if query.lower() in article.lower():
                    list_articles.append(article)

            return render(request, "encyclopedia/search.html", {
                'articles': list_articles
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, article):
    """ Shows the content of the article and redirect to the edition page in case is required"""
    if request.method == "POST":

        path = request.path
        breakpoint()

        title = request.POST['title']

        text = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'text': text
        })

    if article in util.list_entries():
        # Get the article in markdown
        article_md = util.get_entry(article)

        # Convert it to html format using markdown2
        markdowner = Markdown()
        article_html = markdowner.convert(article_md)

        return render(request, "encyclopedia/entries.html", {
            'title': article,
            'content': article_html
        })
    else:
        return HttpResponse("<h1 style='font-size: 80px; text-align: center; margin:50px;'>Article not found<h1>")

def create(request):
    """Creates a new Post"""
    if request.method == "POST":
        data = request.POST

        title = request.POST['title']
        text = request.POST['text']

        if title == '' or text == '':
            return HttpResponse("<h1>Title and Text are required Fields</h1>")

        articles = [article.lower() for article in util.list_entries()]

        if title.lower() in articles:
            return HttpResponse("<h1>Article already exists</h1>")

        util.save_entry(title,text)

        return HttpResponseRedirect(reverse("encyclopedia:index"))

    return render(request, "encyclopedia/create.html")

def edit(request):
    """Edit Articles and save them"""
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']

        util.save_entry(title, text)

        return HttpResponseRedirect(reverse("encyclopedia:index"))


def random(request):
    """Shows a random article"""
    article = choice(util.list_entries())

    return entries(request, article)
