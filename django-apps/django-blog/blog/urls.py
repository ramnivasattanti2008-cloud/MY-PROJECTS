from django.contrib import admin
from django.urls import path, include
from django.views.generic import ListView, DetailView
from .models import Post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListView.as_view(model=Post, template_name='blog/index.html', paginate_by=10), name='post-list'),
    path('post/<int:pk>/', DetailView.as_view(model=Post, template_name='blog/post.html'), name='post-detail'),
    path('category/<slug:slug>/', ListView.as_view(template_name='blog/category.html'), name='category-posts'),
]
