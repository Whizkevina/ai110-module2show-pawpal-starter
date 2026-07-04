from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule(scheduler: Scheduler) -> str:
    """Format today's schedule for terminal output."""
    plan = scheduler.build_plan()
    lines = [f"Today's Schedule for {scheduler.owner.name}:"]

    if not plan:
        lines.append("No tasks fit into today's plan.")
        return "\n".join(lines)

    for index, task in enumerate(plan, start=1):
        pet_name = task.pet.name if task.pet else "Unknown pet"
        lines.append(
            f"{index}. {task.preferred_time or 'Anytime'} - {task.description} "
            f"for {pet_name} ({task.duration_minutes} min, priority: {task.priority})"
        )

    return "\n".join(lines)


def print_task_list(title: str, tasks: list[Task]) -> str:
    """Format a task list for the terminal."""
    lines = [title]
    if not tasks:
        lines.append("- None")
        return "\n".join(lines)

    for task in tasks:
        pet_name = task.pet.name if task.pet else "Unknown pet"
        lines.append(f"- {task.schedule_label()} [{pet_name}]")
    return "\n".join(lines)


def main() -> None:
    """Build a demo owner, pets, and schedule."""
    owner = Owner(name="Jordan", daily_time_budget_minutes=120)

    dog = Pet(name="Mochi", species="dog", age_years=4)
    cat = Pet(name="Pepper", species="cat", age_years=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(description="Feeding", duration_minutes=15, priority="high", preferred_time="09:00", frequency="daily"))
    dog.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", preferred_time="08:00", frequency="daily"))
    cat.add_task(Task(description="Litter box clean", duration_minutes=10, priority="medium", preferred_time="09:30", frequency="daily"))
    cat.add_task(Task(description="Playtime", duration_minutes=20, priority="low", preferred_time="17:00", frequency="weekly"))

    recurring = Task(description="Refill water bowls", duration_minutes=5, priority="medium", preferred_time="18:00", frequency="daily")
    cat.add_task(recurring)

    dog.add_task(Task(description="Vet meds", duration_minutes=5, priority="high", preferred_time="09:00", frequency="weekly"))

    scheduler = Scheduler(owner)

    next_occurrence = scheduler.mark_task_complete(recurring)

    print(print_task_list("All tasks sorted by time:", scheduler.sort_by_time()))
    print()
    print(print_task_list("Tasks for Mochi:", scheduler.filter_tasks(pet_name="Mochi")))
    print()
    print(print_task_list("Completed tasks:", scheduler.filter_tasks(completed=True)))
    print()
    print(print_task_list("Recurring tasks added after completion:", [next_occurrence] if next_occurrence else []))
    print()

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("Conflict warnings:")
        for warning in conflicts:
            print(f"- {warning}")
        print()

    print(format_schedule(scheduler))


if __name__ == "__main__":
    main()