from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class NewPage(forms.Form):
    Subject =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    Body = forms.CharField(widget=forms.Textarea(attrs={
        'class' : "form-control col-md-8 col-lg-8", 'rows' : "10"}))
    edit = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "search":False
    })

def titlesearch(request,title):
    srchfrm = title
    mark = Markdown()
    for entry in util.list_entries():
        if srchfrm.lower() == entry.lower():
            content = util.get_entry(srchfrm)
            return render(request,"encyclopedia/title.html",{
            "title":srchfrm, "content":mark.convert(content)
            })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    mark = Markdown()
    srchfrm = request.GET.get('q','')    
    for entry in util.list_entries():
        if srchfrm.lower() == entry.lower():
            content = util.get_entry(srchfrm)
            return render(request,"encyclopedia/title.html",{
            "title":srchfrm, "content":mark.convert(content)
            })
    possible = []
    for entry in util.list_entries():
        if srchfrm.lower() in entry.lower():
            possible.append(entry)
    return render(request,"encyclopedia/index.html",{
        "searchword":srchfrm, "results":possible, "search":True
    })
            
def newpage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            sub = form.cleaned_data["Subject"]
            body = form.cleaned_data["Body"]
            edit = form.cleaned_data["edit"]
            if edit==True:
                util.save_entry(sub,body)
                return HttpResponseRedirect(reverse("index"))
            if sub not in util.list_entries():
                util.save_entry(sub,body)
                return HttpResponseRedirect(reverse("index"))
            for entry in util.list_entries():
                if entry.lower()==sub.lower():
                    return render(request, "encyclopedia/alerterror.html",{
                    "form":form,"title":sub
                    })
               
                

    return render(request,"encyclopedia/newpage.html",{
        "form":NewPage()
    })

def edit(request,head):
    content = util.get_entry(head)
    form = NewPage()
    form.fields["Subject"].initial = head
    form.fields["Subject"].widget = forms.HiddenInput()
    form.fields["Body"].initial = content
    form.fields["edit"].initial = True
    return render(request,"encyclopedia/newpage.html",{
        "form":form, "title":form.fields["Subject"].initial, "edit":form.fields["edit"].initial
    })

def randompage(request):
    title = random.choice(util.list_entries())
    content = util.get_entry(title)
    mark = Markdown()
    return render(request, 'encyclopedia/title.html',{
        "title":title, "content":mark.convert(content)
    })


        