from datetime import datetime as dt
import os
import time 

tasks = []

def get_current_time():
    return dt.now()  #function to show current time 

def show_header():
    os.system('cls' if os.name == 'nt' else 'clear') # nt comes from windows file system ntfs ... os.system() helps to give direct command to the terminal so run cls if its windows otherwise run clear (nt foor windows and posix for linux / mac) to clear the terminal screen
    print("\n")
    print("====================================================")
    print("   CURRENT DATE & TIME:", get_current_time().strftime("%B %d %Y , %I:%M %p")) #strftime() is used to format the date and time in a specific way. %Y for year, %m for month, %d for day, %I for hour (12-hour format), %M for minute, and %p for AM/PM.
    print("====================================================\n") #%B for full month name, %d for day of the month, %Y for year, %I for hour (12-hour format), %M for minute, and %p for AM/PM.    

def formate_datetime(date, time):
    formats = [
        "%Y-%m-%d  %H:%M",     # 2026-04-12 15:30
        "%d/%m/%Y  %H:%M",     # 12/04/2026 15:30
        "%Y-%m-%d  %I:%M %p",  # 2026-04-12 03:30 PM
        "%d/%m/%Y  %I:%M %p"   # 12/04/2026 03:30 PM
    ]
    
    for fmt in formats: #converts string to date time objects
        try:
            return dt.strptime(f"{date} {time}", fmt) #strptime() is used to parse a string into a datetime object based on the specified format. It takes a string and a format and returns a datetime object if the string matches the format.
        except:
            continue
    return None

def add_task():
    show_header() #to show current date and time when user is adding a task
    name = input('Enter your Task name : ')      
    date = input('Enter date (YYYY-MM-DD or DD/MM/YYYY) : ')
    time = input('Enter time (HH:MM or HH:MM AM/PM) : ')
    
    task_datetime = formate_datetime(date, time)


    if not task_datetime:
        print("Invalid date/time format!")
        input("Press Enter...")
        return
    now = get_current_time()
    if task_datetime < now:
        print("Date/Time has already been passed!")
        input("Press Enter...")
        return
    
    tasks.append({
        "Task Name": name,
        "Task Date & Time": task_datetime,
        "Done": False
    })
    print("Task added successfully!")
    input("Press Enter...")
def view_tasks():
    #show_header()
    if not tasks:
        print("No tasks available.")
        input("Press Enter...")
        return

    print("\nTASK LIST:\n")
    for i , task in enumerate(tasks):#enumerate() is used to loop through the tasks list and get both the index (i) and the task itself (task) in each iteration. This allows us to display the task number along with the task details when printing the task list.
        
        status = "Done" if task["Done"] else "Not Done"
        time_str = task["Task Date & Time"].strftime("%B %m %Y , %I:%M %p") #strftime() is used to format the date and time in a specific way. %B for full month name, %m for month, %Y for year, %I for hour (12-hour format), %M for minute, and %p for AM/PM.
        print(f"{i+1}. {task['Task Name']} | {time_str} | {status}")
   # input("Press Enter...")
    

def mark_done():
    view_tasks()
    try:
        num = int(input("Enter task number to mark done: "))
        if 0 < num <= len(tasks):
            tasks[num-1]["Done"] = True
            print("Task marked as done!")
            
        else:
            print("Invalid task number!")
            
    except ValueError:
        print("Invalid input!")
    input("Press Enter...")

def delete_task():
    view_tasks()
    try:
        num = int(input("Enter task number to delete: "))
        if 0 < num <= len(tasks):
            tasks.pop(num-1)
            print("Task deleted!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Invalid input!")
    input("Press Enter...")

try:
    while True:
        show_header()
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_done()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("Closing the list..... ")
            
            break
        else:
            print("Invalid choice!\n")
            time.sleep(1)  # Pause for a moment before showing the menu again

except KeyboardInterrupt:
    print("\nProgram closed safely.")          
            
            
        
    
    
    
    
    
show_header()
  