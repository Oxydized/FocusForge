from task_parser import extrac_tasks

def main():
    print("Welcome to FocusForge")
    print("Brain dump your tasks below.\n")

    brain_dump = input("What do you need to do? ")

    tasks = extrac_tasks(brain_dump)

    print("\nParsed Tasks:")

    if not tasks:
        print("No tasks found.")
        return
    
    for index, task in enumerate(tasks, start=1):
        due_date = task["due_date"] if task["due_date"] else "No due date"

        print(f"{index}. {task['title']} | Due: {due_date} | Urgency: {task['urgency']}")

if __name__ == "__main__":
    main()