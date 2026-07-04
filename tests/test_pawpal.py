from pawpal_system import Pet, Task


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