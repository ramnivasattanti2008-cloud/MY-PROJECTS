from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    filter_status = request.GET.get('filter')
    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'pending':
        todos = todos.filter(completed=False)
    priority = request.GET.get('priority')
    if priority:
        todos = todos.filter(priority=priority)
    return render(request, 'todo/list.html', {'todos': todos})


@login_required
def todo_create(request):
    if request.method == 'POST':
        Todo.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            priority=request.POST.get('priority', 'medium'),
            due_date=request.POST.get('due_date') or None
        )
        messages.success(request, 'Todo created!')
        return redirect('todo-list')
    return render(request, 'todo/form.html')


@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description', '')
        todo.priority = request.POST.get('priority', 'medium')
        todo.due_date = request.POST.get('due_date') or None
        todo.save()
        messages.success(request, 'Todo updated!')
        return redirect('todo-list')
    return render(request, 'todo/form.html', {'todo': todo})


@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted!')
    return redirect('todo-list')


@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo-list')
