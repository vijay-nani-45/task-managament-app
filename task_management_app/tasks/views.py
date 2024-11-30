from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib import messages

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title:
            Task.objects.create(
                user=request.user, 
                title=title, 
                description=description
            )
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
        else:
            messages.error(request, 'Task title cannot be empty.')
    
    return render(request, 'tasks/task_form.html')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.is_completed = request.POST.get('is_completed') == 'on'
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_form.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')