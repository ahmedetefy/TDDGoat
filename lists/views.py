from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item, List

# Create your views here.
def home_page(request):
    return render(request, "home.html")

def view_list(request):
	return render(request, "list.html", {
        'item_list': Item.objects.all()
        })

def new_list(request):
    list_ = List.objects.create()
    item_text = request.POST['item_text']
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/the-only-list-in-the-world/')