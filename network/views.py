import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    all_posts = Post.objects.order_by("-timestamp")
    all_posts = [post.serialize() for post in all_posts]

    user_posts = None
    liked_posts = None
    if request.user.is_authenticated:
        # the posts that the user can edit
        user_posts = request.user.posts.all()
        user_posts = [post.serialize() for post in user_posts]

        # the posts liked by the user
        liked_posts = request.user.postLikes.order_by("-timestamp")
        liked_posts = [post.serialize() for post in liked_posts]

    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "liked_posts": liked_posts,
        "user_posts": user_posts
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


@login_required
def following(request):
    user = User.objects.get(username=request.user)

    # get all the users I'm following
    users_following = user.userFollowing.all()

    # create an empty QuerySet Post object
    all_posts = Post.objects.none()

    # For each user I'm following get all posts 
    # and append them to the QuerySet
    for user_follow in users_following:
        user_posts = user_follow.posts.all()
        all_posts = all_posts | user_posts

    all_posts = all_posts.order_by("-timestamp")

    # the posts liked by the user
    liked_posts = request.user.postLikes.order_by("-timestamp")

    return render(request, "network/following.html", {
        "all_posts": all_posts,
        "liked_posts": liked_posts
    })


@csrf_exempt
def profile(request, username):
    user = User.objects.get(username=username)

    if request.method == "GET":

        all_posts = user.posts.order_by("-timestamp")

        following = user.userFollowing.count()
        followers = user.followed_by.count()

        # is the user isn't authenticated, then 
        # the button shouldn't be seen at all
        should_show_follow_button = None
        is_user_following = None
        liked_posts = None
        if request.user.is_authenticated:

            # the posts liked by the user
            liked_posts = request.user.postLikes.order_by("-timestamp")
      
            # if the user making the request is not the same 
            # than the one of the profile, show the follow button.
            # This prevents users from following/unfollowing themselves
            should_show_follow_button = True if request.user != user else False

            # if the requesting user is already following 
            # the user whose info is requesting then 
            # isUserFollowing is true, otherwise false
            is_user_following = True if user.followed_by.contains(request.user) else False

        return render(request, "network/profile.html", {
            "username": username,
            "all_posts": all_posts,
            "liked_posts": liked_posts,
            "following": following,
            "followers": followers,
            "should_show_follow_button": should_show_follow_button,
            "is_user_following": is_user_following 
        })
    
    elif request.method == "PUT":
        
        data = json.loads(request.body)        
        isUserFollowing = data["isUserFollowing"]

        # if the requesting user is already following that 
        # particular user, then remove the follow, otherwise add it
        if isUserFollowing: user.followed_by.remove(request.user)
        else: user.followed_by.add(request.user)

        followers = user.followed_by.count() 
        return JsonResponse({
            "isUserFollowing": not isUserFollowing,
            "followers": followers,
        }, status=201)


@csrf_exempt
@login_required
def create(request):

    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get contents of post
    data = json.loads(request.body)
    body = data.get("body", "")

    # Create post
    post = Post(
        author=request.user,
        body=body
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


@csrf_exempt
@login_required
def like(request):

    # Liking/Unliking must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    postId = data["postId"]

    post = Post.objects.get(id=postId)
    isPostLiked = request.user.postLikes.contains(post)

    # if the requesting user is already liking that 
    # particular post, then remove the like, otherwise add it
    if isPostLiked: post.liked_by.remove(request.user) 
    else: post.liked_by.add(request.user)
    
    likeCount = post.liked_by.count()

    return JsonResponse({
        "isPostLiked": not isPostLiked,
        "likeCount": likeCount,
    }, status=201)
 

@csrf_exempt
@login_required
def edit(request):

    # Editing post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    postId = data["postId"]
    postBody = data["postBody"]
    print(type(postBody))

    # TODO: - Updating post body
    # 

    return JsonResponse({"message": "Post edited successfully."}, status=201)
