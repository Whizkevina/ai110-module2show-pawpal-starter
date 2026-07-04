from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    """mark_complete should flip the task to completed."""
    task = Task(description="Morning walk", duration_minutes=30)

    task.mark_complete()

    assert task.completed is True
    assert task.completion_timestamp


def test_adding_task_increases_pet_task_count() -> None:
    """Adding a task should increase the pet task list size."""
    pet = Pet(name="Mochi", species="dog")

    pet.add_task(Task(description="Feeding", duration_minutes=10))

    assert pet.task_count() == 1
    assert pet.care_tasks[0].pet is pet


def test_mark_task_complete_creates_next_recurring_task() -> None:
    """Completing a recurring task should add the next occurrence."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Pepper", species="cat")
    owner.add_pet(pet)

    task = Task(description="Refill water bowls", duration_minutes=5, frequency="daily")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.pet is pet
    assert pet.task_count() == 2