from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import User, Post, Profile


def index(request):
    post_list = Post.objects.order_by("-time")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts":posts
    })


@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        post = Post()
        post.user = User.objects.get(username=request.user.username)
        post.post = request.POST["post_body"]
        post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def profile(request, username):
    user=User.objects.get(username=username)
    post_list = Post.objects.filter(user=user).order_by("-time")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    key_followers = Profile.objects.filter(following=user)
    following = len(Profile.objects.filter(user=user).exclude(following__isnull=True))
    followers = []
    for f in key_followers:
        followers.append(f.user.username)
    Follow = False
    if request.user.username in followers:
        Follow = True
    return render(request, "network/profile.html", {
        "name":user.username,
        "posts":posts,
        "follower":len(key_followers),
        "following":following,
        "Follow":Follow
        
    })


@login_required
def follow(request, name):
    user = User.objects.get(username=request.user.username)
    following = User.objects.get(username=name)
    if request.user.username != name:
        # check if user is already following this person
        if Profile.objects.filter(user=user, following=following):
            profile = Profile.objects.get(user=user, following=following)
            profile.delete()
        else:
            profile = Profile()
            profile.user = user
            profile.following = following
            profile.save()
    return HttpResponseRedirect(reverse("profile", args=[name]))


@login_required
def following(request):
    user=User.objects.get(username=request.user.username)
    followings = Profile.objects.filter(user=user).exclude(following__isnull=True)
    follow_posts_list = []
    for following in followings:
        ps = Post.objects.filter(user=following.following).order_by("-time")
        for p in ps:
            follow_posts_list.append(p)
    paginator = Paginator(follow_posts_list, 10)
    page_number = request.GET.get('page')
    follow_posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "follow_posts":follow_posts
    })


@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=post_id)
            if post.user.username == request.user.username:
                post.post = data.get("post")
                post.save()
                return JsonResponse({
                "post": post.post
                })
            else:
                return JsonResponse({"message": "You cannot edit this post!"},status=403)
        except Post.DoesNotExist:
            return JsonResponse({"message": "Post not found"},status=400)
        


@login_required
def delete(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.user.username == request.user.username:
            post.delete()
            return JsonResponse({
                "message": "Post successfully deleted!",
                'deleted': True
                },status=200)
        else:
            return JsonResponse({"message": "You cannot delete this post!"},status=403)
    except Post.DoesNotExist:
        return JsonResponse({"message": "Post not found"},status=400)


@csrf_exempt
@login_required
def like(request, post_id):
    try:
        liked = None
        post = Post.objects.get(id = post_id)
        user = request.user
        if user in post.likes.all():
                post.likes.remove(user)
                liked = False
        else:
            post.likes.add(user)
            liked = True
        
        return JsonResponse({
                "count": post.likes_count(),
                "liked": liked,
        })
    except:
        return JsonResponse({"message": "Post not found"},status=400)

        
            


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
