from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Item, Bid, Comment


def index(request):    
    item = Item.objects.filter(is_closed=False)
    return render(request, "auctions/index.html", {
        "items": item,
        "categories": Category.objects.all
    })


def index_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    item = Item.objects.filter(category=category, is_closed=False)
    return render(request, "auctions/index.html", {
        "items": item,
        "categories": Category.objects.all
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def sell(request):
    if request.method == "POST":
        user = request.user
        check = []
        
        try:
            category = Category.objects.get(pk=request.POST["category"])
        except:
            return render(request, "auctions/sell.html", {
                "invalid": True
            })

        title = request.POST["title"]
        check.append(title)
        
        description = request.POST["description"]
        check.append(description)
        
        price = request.POST["price"]
        check.append(price)
        
        image_url = request.POST["image"]
        check.append(image_url)

        for field in check:
            if not field:
                return render(request, "auctions/sell.html", {
                    "invalid": True
                })

        item = Item(seller=user, title=title, description=description, start_price=price, category=category,
                    image_url=image_url)
        item.save()
        item.watchers.add(user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/sell.html", {
            "options": Category.objects.all
        })


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    user = request.user
    comments = Comment.objects.filter(item=item)
    flag = True
    if not comments:
        comments = "No comments yet"
        flag = False
    
    if item.current_price:
        bid = Bid.objects.get(item=item, offer=item.current_price) 
        return render(request, "auctions/item.html", {
            "item": item,
            "comments": comments,
            "user": user,
            "bid": bid,
            "flag": flag
        })

    else:
        return render(request, "auctions/item.html", {
            "item": item,
            "comments": comments,
            "user": user,
            "flag": flag
        })


@login_required
def watch(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id)
        user = User.objects.get(pk=int(request.POST["user"]))
        if user in item.watchers.all():
            item.watchers.remove(user)
        else:
            item.watchers.add(user)
        return HttpResponseRedirect(reverse("auctions:item", args=(item.id,)))


@login_required
def comment(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id)
        user = User.objects.get(pk=int(request.POST["user"]))
        comment = request.POST["comment"]
        if comment:
            comments = Comment(item=item, user=user, comment=comment)
            comments.save()
        return HttpResponseRedirect(reverse("auctions:item", args=(item.id,)))


@login_required
def bid(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id)
        user = User.objects.get(pk=int(request.POST["user"]))
        bid = float(request.POST["bid"])
        
        if not item.current_price:
            if bid >= item.start_price and not item.is_closed:
                item.current_price = bid
                item.save()
                offer = Bid(item=item, user=user, offer=bid)
                offer.save()
                item.watchers.add(user)
                return HttpResponseRedirect(reverse("auctions:item", args=(item.id,)))
            else:
                comments = Comment.objects.filter(item=item)
                flag = True
                if not comments:
                    comments = "No comments yet"
                    flag = False
                return render(request, "auctions/item.html", {
                    "item": item,
                    "comments": comments,
                    "user": user,
                    "bid": bid,
                    "flag": flag,
                    "alert": True
                })
        
        else:
            if bid > item.current_price and not item.is_closed:
                item.current_price = bid
                item.save()
                offer = Bid(item=item, user=user, offer=bid)
                offer.save()
                return HttpResponseRedirect(reverse("auctions:item", args=(item.id,)))
            else:
                comments = Comment.objects.filter(item=item)
                flag = True
                if not comments:
                    comments = "No comments yet"
                    flag = False
                return render(request, "auctions/item.html", {
                    "item": item,
                    "comments": comments,
                    "user": user,
                    "bid": bid,
                    "flag": flag,
                    "alert": True
                })


@login_required
def close(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(pk=item_id)
        seller = request.user
        last_bid = Bid.objects.get(item=item, offer=item.current_price)
        if item.current_price and seller.id == item.seller.id and request.POST["close"] == "Close Deal":
            item.is_closed = True
            item.buyer = last_bid.user
            item.save()
    return HttpResponseRedirect(reverse("auctions:index"))


@login_required
def watchlist(request, user_id):
    items = Item.objects.filter(watchers=user_id)
    return render(request, "auctions/watchlist.html", {
        "items": items
    })