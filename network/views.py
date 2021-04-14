import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Follow, Post


def index(request):
    return render(request, "network/index.html", {
        "user": request.user
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            new_follow_block = Follow(user=user)
            new_follow_block.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def send_post(request):
    
    # To write a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get information about the post
    data = json.loads(request.body)
    post = data.get("post")
    user = request.user

    # Add information to database
    if user and post.strip():
        new_post = Post(user=user, post=post)
        new_post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)


def show_post(request, watchers, user_id):
    data = []
    
    # Get user
    user = User.objects.get(pk=int(user_id))

    # Generate list of posts
    if watchers == "all_posts":
        posts = Post.objects.all().order_by("-date")

    elif watchers == "home":
        following = Follow.objects.get(user=user)
        posts = Post.objects.filter(user__in=following.following.all()).order_by("-date")
        print(posts)

    elif watchers == "profile":
        posts = Post.objects.filter(user=user).order_by("-date")

    paginator = Paginator(posts, 10)
    page = paginator.page(int(request.GET.get("page")))

    for i in range(len(page.object_list)):
        data.append([])
        data[i].append(page.object_list[i].serialize())
            
        if request.user in page.object_list[i].likes.all():
            data[i].append(True)
        else:
            data[i].append(False)

    return JsonResponse({
        "posts": data,
        "num_pages": paginator.num_pages
    }, status=202)


@csrf_exempt
@login_required
def like(request):    
    # To like a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get information about the user and the post
    data = json.loads(request.body)
    user = User.objects.get(pk=int(data.get("user_id")))
    post = Post.objects.get(pk=int(data.get("post_id")))
    
    if request.user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        "message": "Database successfully updated",
        "likes": post.likes.count(),
        "liked": liked,
        "post_id": post.id
    }, status=201)


@csrf_exempt
@login_required
def load_profile(request, user_id):
    user = User.objects.get(pk=int(user_id))
    follow = Follow.objects.get(user=user)

    following = []
    followers = []

    for i in follow.followers.all():
        followers.append(i.username)
    for j in follow.following.all():
        following.append(j.username)

    return JsonResponse({
        "following": following,
        "followers": followers,
        "user": user.username,
        "is_following": ((request.user in follow.followers.all()))
    }, status=203)


@csrf_exempt
@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    follow_intent_id = data.get("follow_intent_id")

    follow_intent = User.objects.get(pk=int(follow_intent_id))
    follow_intent_follow_block = Follow.objects.get(user=follow_intent)

    user = request.user
    user_follow_block = Follow.objects.get(user=user)

    if user in follow_intent_follow_block.followers.all() and follow_intent in user_follow_block.following.all():
        follow_intent_follow_block.followers.remove(user)
        user_follow_block.following.remove(follow_intent)

    else:
        follow_intent_follow_block.followers.add(user)
        user_follow_block.following.add(follow_intent)
    
    following = []
    followers = []

    for i in follow_intent_follow_block.followers.all():
        followers.append(i.username)
    for j in follow_intent_follow_block.following.all():
        following.append(j.username)

    return JsonResponse({
        "message": "Database Updated successfully",
        "followers": followers,
        "following": following,
        "is_following": ((user in follow_intent_follow_block.followers.all() and follow_intent in user_follow_block.following.all()))
    }, status=201)


@login_required
@csrf_exempt
def edit_post(request):
    if request.method != 'POST':
        return JsonResponse({"message": "POST request required."}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    post_edit_text = data.get("postEditText")
    
    post = Post.objects.get(pk=int(post_id))

    if request.user.id != user_id or post.user.id != request.user.id:
        return JsonResponse({"message": "Can´t edit other user post"}, status=400)

    post.post = post_edit_text
    post.save()

    return JsonResponse({
        "message": "Post successfully updated in database",
        "editedText": post_edit_text
    }, status=203)