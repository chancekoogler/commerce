from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import *

class CreateListing(forms.Form):       
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.CharField(label="Image URL", max_length=500)
    price = forms.CharField(label="Starting Price ($)", max_length=12)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    

class Bid(forms.Form):
    bid = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Place Bid'}))
    watchList = forms.BooleanField(required=False)
    comment = forms.CharField(required=False, widget=forms.Textarea)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
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
    
    
def create(request):
    return render(request, "auctions/create.html", {
        "form": CreateListing()
    })
    
def listings(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            image = form.cleaned_data['image']
            price = form.cleaned_data['price']
            category = Category.objects.get(id=int(request.POST['category']))
            instance = Auction(title=title, description=desc, image=image, price=price, owner=str(request.user), isOpen=True, category=category)
            instance.save()
            return render(request, "auctions/listing.html", {
                "listings": Auction.objects.filter(isOpen=True)
            })
    else:
        return render(request, "auctions/listing.html", {
            "listings": Auction.objects.filter(isOpen=True)
        })
    
def item(request, item_id):
    item = Auction.objects.get(pk=item_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            form = Bid(request.POST)
            if form.is_valid():
                if 'watchList' in request.POST and request.POST['bid'] == '':
                    return(addToWatchlist(request, item_id, item, form))
                elif request.POST['bid'] != '' and 'watchList' not in request.POST:
                    return(addBid(request, item_id, item, form))
                elif request.POST['bid'] != '' and 'watchList' in request.POST:
                    return(bidAndWatchlist(request, item_id, item, form))
                else:
                    if request.POST['comment'] != '':
                        current_user = User.objects.get(username=request.user)
                        clean_comment = form.cleaned_data['comment']
                        commentInstance = Comments(user=str(request.user), comment=clean_comment)
                        commentInstance.save()
                        commentInstance.auction.add(item)
                        commentInstance.save()
                        itemsComs = Comments.objects.filter(auction=(item))
                        return render(request, "auctions/item.html", {
                            "item": item,
                            "bid": Bid(),
                            "logged": True,
                            "notice": "Error. Place a bid or add to watchlist before submitting.",
                            "owner": ifOwner(request, item),
                            "comments": itemsComs
                        })
        else:
            if str(request.user) == str(item.winner):
                return render(request, "auctions/item.html", {
                    "item": item,
                    "winner": "You have won this auction. Congratulations!"
            })
            else:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "bid": Bid(),
                    "logged": True,
                    "owner": ifOwner(request, item),
                    "comments": Comments.objects.filter(auction=(item))
                })
    else:
        return render(request, "auctions/item.html", {
            "item": item,
            "bid": Bid(),
            "logged": False,
            "comments": Comments.objects.filter(auction=(item))

        })
        

def watchlist(request):
    current_user = User.objects.get(username=request.user)
    watchList = current_user.watchList.all()
    if request.method == "POST":
        if 'watchList' in request.POST: 
            for i in request.POST['watchList']:
                item = Auction.objects.get(id=i)
                current_user.watchList.remove(item)
            return render(request, "auctions/watchlist.html", {
                "items": watchList
            })
        # if user submitted nothing
        else:
            return render(request, "auctions/watchList.html", {
                "items": watchList
            })
            
    else:
        return render(request, "auctions/watchlist.html", {
            "items": watchList
        })
      
        
def addToWatchlist(request, item_id, item, form):
    current_user = User.objects.get(username=request.user)
    current_user.watchList.add(item)
    current_user.save()
    clean_comment = form.cleaned_data['comment']
    commentInstance = Comments(comment=clean_comment, user=str(request.user))
    commentInstance.save()
    commentInstance.auction.add(item)
    commentInstance.save()
    return render(request, "auctions/item.html", {
        "item": item,
        "bid": Bid(),
        "logged": True,
        "owner": ifOwner(request, item),
        "comments": Comments.objects.filter(auction=(item))

    })


def addBid(request, item_id, item, form):
    clean_comment = form.cleaned_data['comment']
    clean_bid = form.cleaned_data['bid']
    counter = 0
    all_bids = Bids.objects.filter(auction=item)
    current_user = User.objects.get(username=request.user)
    clean_comment = form.cleaned_data['comment']
    commentInstance = Comments(comment=clean_comment, user=request.user)
    commentInstance.save()
    commentInstance.auction.add(item)
    commentInstance.save()
    for bid in all_bids:
        if clean_bid > item.price and clean_bid > bid.bid:
            counter += 1
    if counter == len(all_bids):
        current_user = User.objects.get(username=request.user)
        instance = Bids(bid=clean_bid, user=current_user)
        instance.save()
        instance.auction.add(item)
        instance.save()
        success = "Bid placed successfully"
        return render(request, "auctions/item.html", {
            "item": item,
            "bid": Bid(),
            "logged": True,
            "notice": success,
            "owner": ifOwner(request, item),
            "comments": Comments.objects.filter(auction=(item))
        })
    else:
        current_user = User.objects.get(username=request.user)
        clean_comment = form.cleaned_data['comment']
        commentInstance = Comments(comment=clean_comment, user=request.user)
        commentInstance.save()
        commentInstance.auction.add(item)
        commentInstance.save()
        error = "Error. Bid must be greater than starting price and greater than highest existing bid. Please try again."
        return render(request, "auctions/item.html", {
            "item": item,
            "bid": Bid(),
            "logged": True,
            "notice": error,
            "owner": ifOwner(request, item),
            "comments": Comments.objects.filter(auction=(item))

        })


def bidAndWatchlist(request, item_id, item, form):
    
    current_user = User.objects.get(username=request.user)
    current_user.watchList.add(item)
    current_user.save()
    clean_bid = form.cleaned_data['bid']
    counter = 0
    all_bids = Bids.objects.filter(user=request.user)
    commentInstance = Comments(comment=clean_comment, user=current_user)
    commentInstance.save()
    commentInstance.auction.add(item)
    commentInstance.save()
    for bid in all_bids:
        if clean_bid > item.price and clean_bid > bid.bid:
            counter += 1
    if counter == len(all_bids):
        current_user = User.objects.get(username=request.user)
        instance = Bids(bid=clean_bid, user=str(current_user))
        instance.save()
        instance.auction.add(item)
        instance.save()
        success = "Bid placed successfully"
        return render(request, "auctions/item.html", {
            "item": item,
            "bid": Bid(),
            "logged": True,
            "notice": success,
            "owner": ifOwner(request, item),
            "comments": Comments.objects.filter(auction=(item))

            })
    else:
        error = "Error. Bid must be greater than starting price and greater than highest existing bid. Please try again."
        return render(request, "auctions/item.html", {
            "item": item,
            "bid": Bid(),
            "logged": True,
            "notice": error,
            "owner": ifOwner(request, item),
            "comments": Comments.objects.filter(auction=(item))

        })


def ifOwner(request, item):
    if str(item.owner) == str(request.user):
        return True
    else:
        return False
    
    
def closeAuction(request, item_id):
    item = Auction.objects.get(id=item_id)
    bidd = Bids.objects.filter(auction=item)
    winningValue = 0
    bids = bidd.values_list('bid', flat=True)
    # have winning Value just have to connect it to auction db
    # and declare winner
    for i in bids:
        if i > winningValue:
            winningValue = i
    winner = Bids.objects.get(bid=winningValue).user
    item.winner = winner
    item.isOpen = False
    item.save()
   # Auction.objects.filter(pk=item_id).update(isOpen=False)
    return render(request, "auctions/listing.html", {
        "listings": Auction.objects.filter(isOpen=True)
    })

def category(request):
    allCat = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories": allCat
    })
    
def itemsOfCat(request, category):
    category = Category.objects.get(title=category)
    items = Auction.objects.filter(category=category)
    return render(request, "auctions/itemsOfCat.html", {
        "items": items,
        "category": category
    })
