from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Watchlist, Comment



class NewTitleForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "form-control col-md-8 col-lg-8",
        "placeholder": "Title"}))

class NewEntryForm(forms.Form):
    entry = forms.CharField(label='', widget=forms.Textarea(attrs={
        "class": "form-control col-md-8 col-lg-8",
        'rows': 10,
        "placeholder": "Insert Text"}))

class NewCommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={
        "class": "form-control col-md-8 col-lg-8",
        'rows': 5,
        "placeholder": "Insert Text"}))

class NewPriceForm(forms.Form):
    price = forms.FloatField(label='', widget=forms.NumberInput(attrs={
        "class": "form-control col-md-8 col-lg-8",
        'rows': 20,
        "min": 0,
        "placeholder": "Insert Price"}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(listing_status=True),
        "status": True
    })

def close(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(listing_status=False),
        "status": False
    })

def category(request,category_id):
    
    if category_id == 0:
        categories = Category.objects.all()
        return render(request, "auctions/category.html", {
            "categories": categories,
            "status": False
        })
    else:
        categories = Category.objects.get(pk=category_id)
        listing = Listing.objects.filter(group=category_id,listing_status=True)
        return render(request, "auctions/category.html", {
            "listings": listing,
            "category": categories,
            "status": True
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form_item = NewTitleForm(request.POST)
        form_description = NewEntryForm(request.POST)
        form_price = NewPriceForm(request.POST)
        if request.POST.get('image_link'):
           link = request.POST.get('image_link')
        else:
            link = "https://cdn-icons-png.flaticon.com/512/3125/3125669.png"

        
        if form_item.is_valid() and form_description.is_valid() and form_price.is_valid():
            item = form_item.cleaned_data["title"]
            description = form_description.cleaned_data["entry"]
            price = form_price.cleaned_data["price"]
    

            listing = Listing()
            listing.creators = request.user
            listing.item = item
            listing.description = description
            listing.price = price
            listing.link = link
            listing.group = Category.objects.get(pk=int(request.POST["category"]))
            listing.save()

            return HttpResponseRedirect(reverse("index"))


    return render(request, "auctions/create.html", {
        "title": NewTitleForm(),
        "entry": NewEntryForm(),
        "price": NewPriceForm(),
        "categories": categories,
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    show = listing.get_comments.all()
    
    if request.method == "POST":
        status = request.POST.get("status", False)
        form_bid = NewPriceForm(request.POST)
        form_comment = NewCommentForm(request.POST)
        message = False
        if form_bid.is_valid():
            bids = form_bid.cleaned_data["price"]

            if int(bids) > int(listing.price) and int(bids) > int(listing.bid):
                listing.bid = bids
                listing.bidder = request.user
                listing.save()
                message = False
            else:
                message = True 

        if form_comment.is_valid():
            write = form_comment.cleaned_data["comment"]

            comments = Comment()
            comments.writer = request.user
            comments.listing = listing
            comments.comment = write
            comments.save()

        

        auction_status = request.POST.get("auction")
        if auction_status == "Close Auction":
            listing.listing_status = False
            listing.save()
           
        if status == "Add to Watchlist":
            watchlists = Watchlist()
            watchlists.watcher = request.user
            watchlists.watchlist = listing
            watchlists.save()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": NewPriceForm(),
                "comment": NewCommentForm(),
                "show": show,
                "message": message,
                "status": "Remove from Watchlist"
            })
        elif status == "Remove from Watchlist":
            Watchlist.objects.filter(watcher = request.user, watchlist=listing).delete()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": NewPriceForm(),
                "comment": NewCommentForm(),
                "show": show,
                "message": message,
                "status": "Add to Watchlist"
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": NewPriceForm(),
                "comment": NewCommentForm(),
                "message": message,
                "show": show,
                "status": "Add to Watchlist"
            })

    if request.user.is_authenticated:
        if not Watchlist.objects.filter(watcher=request.user, watchlist=listing):
            status = "Add to Watchlist"
        else:
            status = "Remove from Watchlist"
    else:
        status = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": NewPriceForm(),
        "comment": NewCommentForm(),
        "show": show,
        "status": status
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlists": Watchlist.objects.filter(watcher=request.user)
        
    })
