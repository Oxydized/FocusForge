from task_parser import extract_tasks

def print_tasks(text):
    tasks = extract_tasks(text)

    print("\nINPUT:")
    print(text)

    print("\nOUTPUT:")
    for task in tasks:
        print(
            f"- {task['title']} | Due: {task['due_date']} | Urgency: {task['urgency']}"
        )

print_tasks(
    "I should finish my resume Friday and remember to call the doctor tomorrow and don't forget to pay the electric bill today."
)

print_tasks(
    "I need to finish my resume before next week and pay the electric bill before Friday."
)

print_tasks(
    "Research Docker pros and cons and write notes tomorrow."
)