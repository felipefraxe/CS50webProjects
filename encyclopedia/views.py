from django.forms.fields import CharField
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from random import randint

from . import util


class NewForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class": "form-control col-md-8"}))
    content = forms.CharField(label="Markdown content", widget=forms.Textarea(attrs={"class": "form-control col-md-8", "rows": 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/content.html", {
            "title": title,
            "entry": markdown(util.get_entry(title))
    })
    return render(request, "encyclopedia/error.html")


def search(request):
    search = request.GET.get("q")
    if util.get_entry(search):
        return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": search}))
    sub_string = []
    for entry in util.list_entries():
        if search.upper() in entry.upper():
            sub_string.append(entry)
    if len(sub_string) > 0:
        return render(request, "encyclopedia/search.html", {
            "entries": sub_string
        })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": None}))

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            edit = form.cleaned_data["edit"]
            if not util.get_entry(title) or edit:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "exist": True
                })
    return render(request, "encyclopedia/new_page.html", {
        "form": NewForm()
    })

def edit(request, title):
    if not util.get_entry(title):
        return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": None}))
    form = NewForm()
    form.fields["title"].initial = title
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = util.get_entry(title)
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/new_page.html", {
        "subject": title,
        "form": form,
        "edit": form.fields["edit"]
    })


def random(request):
    title = util.list_entries()[randint(0, len(util.list_entries())) - 1]
    return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title": title}))
