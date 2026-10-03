from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Profile, Post, Follow


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created! Complete your profile.')
            return redirect('edit-profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def feed(request):
    following = request.user.following_set.values_list('following', flat=True)
    posts = Post.objects.filter(author__in=list(following) + [request.user.id])
    return render(request, 'social/feed.html', {'posts': posts})


@login_required
def explore(request):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'social/explore.html', {'posts': posts, 'users': users})


@login_required
def create_post(request):
    if request.method == 'POST':
        Post.objects.create(
            author=request.user,
            content=request.POST.get('content', ''),
            image=request.FILES.get('image')
        )
        messages.success(request, 'Post created!')
    return redirect('feed')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'social/post_detail.html', {'post': post})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    followers_count = user.followers_set.count()
    following_count = user.following_set.count()
    return render(request, 'social/profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    })


@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()
    profile = request.user.profile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.website = request.POST.get('website', '')
        if request.FILES.get('picture'):
            profile.profile_picture = request.FILES.get('picture')
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile', username=request.user.username)
    return render(request, 'social/edit_profile.html', {'profile': profile})


@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user)
        messages.success(request, f'Following {user.username}!')
    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user).delete()
    messages.success(request, f'Unfollowed {user.username}.')
    return redirect('profile', username=username)


@login_required
def followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers_set.all()
    return render(request, 'social/followers.html', {'user': user, 'followers': followers})


@login_required
def following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following_set.all()
    return render(request, 'social/following.html', {'user': user, 'following': following})
