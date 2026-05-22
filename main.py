from task_parser import extract_tasks
from storage import save_tasks, load_tasks

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

        print(f"{index}. {task['title']} | Due: {due_date} | Urgency: {task['urgency']}")

    print(f"\nSaved {len(new_tasks)} new task(s).")
    print(f"Total saved tasks: {len(all_tasks)}")

if __name__ == "__main__":
    main()