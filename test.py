from datetime import datetime

tasks = []

def parse_datetime(date, time):
    formats = [
        "%Y-%m-%d %H:%M",     # 2026-04-12 15:30
        "%d/%m/%Y %H:%M",     # 12/04/2026 15:30
        "%Y-%m-%d %I:%M %p",  # 2026-04-12 03:30 PM
        "%d/%m/%Y %I:%M %p"   # 12/04/2026 03:30 PM
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(f"{date} {time}", fmt)
        except:
            continue
    return None

def add_task():
    name = input("Enter task: ")
    date = input("Enter date (YYYY-MM-DD or DD/MM/YYYY): ")
    time = input("Enter time (HH:MM or HH:MM AM/PM): ")

    task_datetime = parse_datetime(date, time)

    if task_datetime:
        tasks.append({
            "task": name,
            "time": task_datetime,
            "done": False
        })
        print("Task added successfully!\n")
    else:
        print("Invalid date/time format!\n")

def view_tasks():
    if not tasks:
        print("No tasks available.\n")
        return

    print("\n📋 Your Tasks:")
    for i, task in enumerate(tasks):
        status = "✔" if task["done"] else "✘"
        time_str = task["time"].strftime("%Y-%m-%d %I:%M %p")
        print(f"{i+1}. {task['task']} | {time_str} | {status}")
    print()

def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        if 0 < num <= len(tasks):
            tasks[num-1]["done"] = True
            print("Task marked as done!\n")
        else:
            print("Invalid task number!\n")
    except:
        print("Please enter a valid number!\n")

def delete_task():
    view_tasks()
    try:
        num = int(input("Enter task number to delete: "))
        if 0 < num <= len(tasks):
            tasks.pop(num-1)
            print("Task deleted!\n")
        else:
            print("Invalid task number!\n")
    except:
        print("Please enter a valid number!\n")

# Main loop
while True:
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Done")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Closing the list.....")
        break
    else:
        print("Invalid choice!\n")