import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Function to add a task to the chart


def add_task(ax, task_name, start_date, end_date, y_position, color):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    ax.broken_barh([(mdates.date2num(start), (mdates.date2num(
        end) - mdates.date2num(start)))], (y_position, 4), facecolors=color)

# Function to adjust task start date based on dependencies


def adjust_start_date(task, tasks_dict):
    dependencies = task.get('dependencies', [])
    latest_end_date = task['start_date']
    for dep in dependencies:
        dep_end_date = tasks_dict[dep]['end_date']
        if dep_end_date > latest_end_date:
            latest_end_date = dep_end_date
    return max(task['start_date'], latest_end_date + timedelta(days=1))

# Main function to create Gantt chart


def create_gantt_chart(tasks):
    fig, ax = plt.subplots(figsize=(10, 5))
    y_positions = []
    task_names = [task['name'] for task in tasks]
    tasks_dict = {task['name']: task for task in tasks}

    # Adjust start dates based on dependencies
    for task in tasks:
        task['start_date'] = adjust_start_date(task, tasks_dict)

    for i, task in enumerate(tasks):
        y_position = 10 * (i + 1)
        y_positions.append(y_position)
        add_task(ax, task['name'], task['start_date'].strftime(
            '%Y-%m-%d'), task['end_date'].strftime('%Y-%m-%d'), y_position, 'tab:blue')

    ax.set_yticks(y_positions)
    ax.set_yticklabels(task_names)
    ax.set_ylim(5, max(y_positions) + 5)
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()


# Example usage
tasks = [
    {'name': "Task 1", 'start_date': datetime(
        2023, 1, 1), 'end_date': datetime(2023, 1, 10)},
    {'name': "Task 2", 'start_date': datetime(2023, 1, 5), 'end_date': datetime(
        2023, 1, 15), 'dependencies': ['Task 1']},
    # Add more tasks with dependencies as needed
]

create_gantt_chart(tasks)
