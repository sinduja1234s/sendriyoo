from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .models import Task
from django.http import JsonResponse

def home(request):
    tasks = Task.objects.order_by('deadline')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    completion_percentage = round(
    (completed_tasks / total_tasks) * 100
) if total_tasks else 0
    overdue_tasks = tasks.filter(
        completed=False,
        deadline__lt=timezone.now()
    ).count()
    due_today = tasks.filter(
        completed=False,
        deadline__date=timezone.localdate()
    ).count()

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'due_today': due_today,
    })


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        deadline_text = request.POST.get('deadline', '')
        deadline = parse_datetime(deadline_text) if deadline_text else None

        if title and deadline:
            if timezone.is_naive(deadline):
                deadline = timezone.make_aware(deadline)

            Task.objects.create(
                title=title,
                description=description,
                deadline=deadline
            )
            return redirect('home')

    return render(request, 'add_task.html')


def toggle_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save(update_fields=['completed'])

    return redirect('home')


def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()

    return redirect('home')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        deadline_text = request.POST.get('deadline', '')
        deadline = parse_datetime(deadline_text) if deadline_text else None

        if title and deadline:
            if timezone.is_naive(deadline):
                deadline = timezone.make_aware(deadline)

            task.title = title
            task.description = description
            task.deadline = deadline
            task.save()
            return redirect('home')

    return render(request, 'edit_task.html', {'task': task})
def check_reminders(request):
    if request.method != 'POST':
        return JsonResponse({'reminders': []})

    today = timezone.localdate()
    reminders = []

    tasks = Task.objects.filter(completed=False)

    for task in tasks:
        deadline_date = timezone.localtime(task.deadline).date()
        days_left = (deadline_date - today).days

        if days_left == 2 and not task.reminder_2_days_sent:
            message = f"{task.title} is due in 2 days!"
            task.reminder_2_days_sent = True
            reminders.append(message)

        elif days_left == 1 and not task.reminder_1_day_sent:
            message = f"{task.title} is due tomorrow!"
            task.reminder_1_day_sent = True
            reminders.append(message)

        elif days_left == 0 and not task.reminder_today_sent:
            message = f"{task.title} is due today!"
            task.reminder_today_sent = True
            reminders.append(message)

        task.save(update_fields=[
            'reminder_2_days_sent',
            'reminder_1_day_sent',
            'reminder_today_sent'
        ])

    return JsonResponse({'reminders': reminders})