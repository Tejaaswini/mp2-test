import sys
import math
from collections import deque

class Task:
    def __init__(self, name, phase, period, execution_time, deadline):
        self.name = name
        self.phase = int(phase)
        self.period = int(period)
        self.execution_time = int(execution_time)
        self.deadline = int(deadline)
        self.remaining_time = int(execution_time)
        self.next_release = int(phase)
        self.absolute_deadline = int(phase) + int(deadline)

    def __repr__(self):
        return f"{self.name}({self.phase}, {self.period}, {self.execution_time}, {self.deadline})"


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def calculate_hyperperiod(tasks):
    periods = [task.period for task in tasks]
    hyperperiod = periods[0]
    for period in periods[1:]:
        hyperperiod = lcm(hyperperiod, period)
    return hyperperiod


def calculate_utilization(tasks):
    return sum(task.execution_time / task.period for task in tasks)


def utilization_bound(n):
    return n * (2 ** (1 / n) - 1)


def check_schedulability(tasks, algorithm):
    U = calculate_utilization(tasks)
    if algorithm == "rm":
        UB = utilization_bound(len(tasks))
        return U, UB, U < UB
    elif algorithm == "edf":
        return U, 1, U <= 1


def rate_monotonic_scheduling(tasks, hyperperiod):
    timeline = []
    ready_queue = deque()
    current_task = None

    for time in range(hyperperiod):
        for task in tasks:
            if time == task.next_release:
                task.remaining_time = task.execution_time
                task.absolute_deadline = time + task.deadline
                ready_queue.append(task)
                ready_queue = deque(sorted(ready_queue, key=lambda t: t.period))

        if current_task and current_task.remaining_time == 0:
            current_task = None
        if not current_task and ready_queue:
            current_task = ready_queue.popleft()
        
        if current_task:
            current_task.remaining_time -= 1
            timeline.append((time, current_task.name))
        else:
            timeline.append((time, "0"))
        
        for task in list(ready_queue):
            if time == task.absolute_deadline and task.remaining_time > 0:
                timeline.append((time, f"DEADLINE_MISS({task.name})"))
                ready_queue.remove(task)
    
    return timeline


def earliest_deadline_first_scheduling(tasks, hyperperiod):
    timeline = []
    ready_queue = deque()
    current_task = None
    
    for time in range(hyperperiod):
        for task in tasks:
            if time == task.next_release:
                task.remaining_time = task.execution_time
                task.absolute_deadline = time + task.deadline
                ready_queue.append(task)
                ready_queue = deque(sorted(ready_queue, key=lambda t: t.absolute_deadline))

        if current_task and current_task.remaining_time == 0:
            current_task = None
        if not current_task and ready_queue:
            current_task = ready_queue.popleft()
        
        if current_task:
            current_task.remaining_time -= 1
            timeline.append((time, current_task.name))
        else:
            timeline.append((time, "0"))
        
        for task in list(ready_queue):
            if time == task.absolute_deadline and task.remaining_time > 0:
                timeline.append((time, f"DEADLINE_MISS({task.name})"))
                ready_queue.remove(task)
    
    return timeline


def main():
    if len(sys.argv) < 7:
        print("Usage: python3 mp1.py -i <input_file> -e <algorithm> -o <output_file>")
        sys.exit(1)
    
    input_file, algorithm, output_file = sys.argv[2], sys.argv[4], sys.argv[6]
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    tasks = []
    for line in lines:
        name, phase, period, execution_time, deadline = line.strip().split(', ')
        tasks.append(Task(name, phase, period, execution_time, deadline))
    
    hyperperiod = calculate_hyperperiod(tasks)
    U, UB, schedulable = check_schedulability(tasks, algorithm)
    
    if algorithm == "rm":
        schedule = rate_monotonic_scheduling(tasks, hyperperiod)
    else:
        schedule = earliest_deadline_first_scheduling(tasks, hyperperiod)
    
    with open(output_file, 'w') as f:
        f.write(f"{algorithm.upper()}\n")
        f.write("SCHEDULABLE\n" if schedulable else "NOT SCHEDULABLE\n")
        f.write(f"U = {U:.3f}\n")
        f.write(f"UB = {UB:.3f}\n\n")
        for entry in schedule:
            f.write(f"{entry[0]} {entry[1]}\n")

if __name__ == "__main__":
    main()