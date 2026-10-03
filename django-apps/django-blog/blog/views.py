from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Post, Comment


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            author_name=request.POST.get('author_name'),
            content=request.POST.get('content')
        )
        messages.success(request, 'Comment added!')
        return redirect('post-detail', pk=pk)
    return render(request, 'blog/post.html', {'post': post})
