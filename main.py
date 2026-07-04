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


def main() -> None:
    """Build a demo owner, pets, and schedule."""
    owner = Owner(name="Jordan", daily_time_budget_minutes=120)

    dog = Pet(name="Mochi", species="dog", age_years=4)
    cat = Pet(name="Pepper", species="cat", age_years=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", preferred_time="08:00"))
    dog.add_task(Task(description="Feeding", duration_minutes=15, priority="high", preferred_time="09:00"))
    cat.add_task(Task(description="Litter box clean", duration_minutes=10, priority="medium", preferred_time="09:30"))
    cat.add_task(Task(description="Playtime", duration_minutes=20, priority="low", preferred_time="17:00"))

    scheduler = Scheduler(owner)
    print(format_schedule(scheduler))


if __name__ == "__main__":
    main()