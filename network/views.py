from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Opinion, Tag

def index(request):

    if request.method == "POST":
        opinion = Opinion()
        opinion.user = request.user
        opinion.title = request.POST["opinion_title"]
        opinion.body = request.POST["opinion_body"]
        opinion.save()
        tags = request.POST["opinion_tags"].split("#")
        for i in tags[1:]:
            if i.strip():
                tag, created = Tag.objects.get_or_create(tag=i.strip())
                opinion.tags.add(tag)

    if request.path == "/following":
        opinions = Opinion.objects.filter(user__in = request.user.following.all()).order_by('-date')
        current_page = "following"
    else:
        opinions = Opinion.objects.all().order_by('-date')
        current_page = "index"

    p = Paginator(opinions, 1)
    try:
        page_no = request.GET.get('page',1) 
        page = p.page(page_no)
    except:
        return redirect('index')
    
    return render(request, "network/index.html", {
        "opinions" : page,
        "current_page" : current_page
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        raise Http404    
    
    if request.method == "PUT":
        if request.headers["Source"] == "follow_unfollow":
            if (user in request.user.following.all()):
                request.user.following.remove(user)
                return JsonResponse({"performed" : "unfollow"})
            else:
                request.user.following.add(user)
                return JsonResponse({"performed" : "follow"})
        
            #another method
            # data = json.loads(request.body.decode('utf-8'))
            # if (data.get("task") == "follow"):
            #     request.user.following.add(user)
            # else:
            #     request.user.following.remove(user)

            # return JsonResponse({"performed" : data.get("task")})
    
    return render(request, "network/profile.html", {
        "profile" : user,
        "profile_posts" : user.user_posts.all().order_by('-date')
    })
