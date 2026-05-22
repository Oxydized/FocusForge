from task_parser import extract_tasks
from storage import (
    save_tasks,
    load_tasks,
    mark_task_completed,
    get_incomplete_tasks,
    get_completed_tasks,
    get_high_urgency_tasks
)


def main():
    print("Welcome to FocusForge")
    print("Brain dump your tasks below.\n")

    existing_tasks = load_tasks()

    brain_dump = input("What do you need to do? ")

    new_tasks = extract_tasks(brain_dump)

    all_tasks = existing_tasks + new_tasks

    save_tasks(all_tasks)

    print("\nParsed Tasks:")

    if not new_tasks:
        print("No tasks found.")
        return
    
    for index, task in enumerate(new_tasks, start=1):
        due_date = task["due_date"] if task["due_date"] else "No due date"

        print(
            f"{index}. "
            f"ID: {task['id'][:8]} | "
            f"{task['title']} | "
            f"Due: {due_date} | "
            f"Urgency: {task['urgency']} | "
            f"Completed: {task['completed']}"
        )

    print(f"\nSaved {len(new_tasks)} new task(s).")
    print(f"Total saved tasks: {len(all_tasks)}")

    while True:
        complete_task = input("\nEnter task ID to mark complete (or press Enter to stop): ").strip()

        if not complete_task:
            break

        task_found = mark_task_completed(complete_task)

        if task_found:
            print("Task marked as completed.")
        else:
            print("No matching task ID found.")

    print("\n=== HIGH PRIORITY TASKS ===")

    high_priority_tasks = get_high_urgency_tasks()

    if high_priority_tasks:
        for task in high_priority_tasks:
            print(f"- {task['title']}")
    else:
        print("No high priority tasks.")

    print("\n=== ACTIVE TASKS ===")

    active_tasks = get_incomplete_tasks()

    if active_tasks:
        for task in active_tasks:
            due_date = task["due_date"] if task["due_date"] else "No due date"

            print(
                f"- {task['title']} | "
                f"Due: {due_date} | "
                f"Urgency: {task['urgency']}"
            )
    else:
        print("No active tasks.")

    print("\n=== COMPLETED TASKS ===")

    completed_tasks = get_completed_tasks()

    if completed_tasks:
        for task in completed_tasks:
            print(f"- {task['title']}")
    else:
        print("No copmpleted tasks.")

if __name__ == "__main__":
    main()