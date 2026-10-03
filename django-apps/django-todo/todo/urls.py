from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('', views.todo_list, name='todo-list'),
    path('todo/create/', views.todo_create, name='todo-create'),
    path('todo/<int:pk>/update/', views.todo_update, name='todo-update'),
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo-delete'),
    path('todo/<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]
