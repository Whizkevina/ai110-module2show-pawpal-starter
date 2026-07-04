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


def test_sort_by_time_returns_chronological_order() -> None:
    """Tasks should be sorted by preferred time first."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Later task", duration_minutes=10, priority="low", preferred_time="18:00"))
    pet.add_task(Task(description="Earlier task", duration_minutes=15, priority="high", preferred_time="08:00"))
    pet.add_task(Task(description="Middle task", duration_minutes=20, priority="medium", preferred_time="12:00"))

    scheduler = Scheduler(owner)

    assert [task.preferred_time for task in scheduler.sort_by_time()] == ["08:00", "12:00", "18:00"]


def test_filter_tasks_by_pet_name_and_completion_status() -> None:
    """Filtering should isolate one pet and one completion state."""
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    pepper = Pet(name="Pepper", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(pepper)

    walk = Task(description="Walk", duration_minutes=30, preferred_time="08:00")
    nap = Task(description="Nap", duration_minutes=20, preferred_time="14:00")
    mochi.add_task(walk)
    pepper.add_task(nap)
    walk.mark_complete()

    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(pet_name="Mochi") == [walk]
    assert scheduler.filter_tasks(completed=True) == [walk]
    assert scheduler.filter_tasks(completed=False) == [nap]
    assert scheduler.filter_tasks(pet_name="Ghost") == []


def test_detect_conflicts_reports_duplicate_times() -> None:
    """Tasks scheduled for the same time should produce a warning."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Pepper", species="cat")
    owner.add_pet(pet)

    pet.add_task(Task(description="Feeding", duration_minutes=10, preferred_time="09:00"))
    pet.add_task(Task(description="Medication", duration_minutes=5, preferred_time="09:00"))

    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == ["Conflict at 09:00: Pepper, Pepper"]


def test_empty_owner_has_no_tasks_or_conflicts() -> None:
    """An owner without pets should yield empty task and conflict results."""
    scheduler = Scheduler(Owner(name="Jordan"))

    assert scheduler.collect_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.detect_conflicts() == []


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