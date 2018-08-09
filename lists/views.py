from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item

# Create your views here.
def home_page(request):
    if request.method == "POST":
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect('/lists/the-only-list-in-the-world/')

    return render(request, "home.html")

def view_list(request):
	return render(request, "list.html", {
        'item_list': Item.objects.all()
        })
    