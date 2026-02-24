from django.db import transaction
from .models import Lion, Task


@transaction.atomic
def create_lion_with_default_tasks(name, track):
    lion = Lion.objects.create(name=name, track=track)

    default_tasks = ["기초 과제", "중급 과제", "심화 과제"]

    for title in default_tasks:
        Task.objects.create(lion=lion, title=title)

    return lion


def toggle_task(task):
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    return task