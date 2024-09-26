from ortools.sat.python import cp_model

# Sample Data
departments = {
    'SOT': ['CSE', 'EC', 'ICT'],
    'SPT': ['Petroleum', 'Mechanical'],
    'SLS': ['Arts', 'Science']
}
semesters = ['Sem1', 'Sem2', 'Sem3', 'Sem4']
subjects = {
    'CSE': ['Math', 'Programming'],
    'EC': ['Circuits'],
    'ICT': ['Networking'],
    'Petroleum': ['Fluid Mechanics'],
    'Mechanical': ['Thermodynamics'],
    'Arts': ['History'],
    'Science': ['Physics']
}
rooms = {
    'BlockA': ['E202', 'E203'],
    'BlockB': ['E204', 'E205']
}
room_capacity = {
    'E202': 30,
    'E203': 25,
    'E204': 20,
    'E205': 15
}
class_times = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-1:00']

# Initialize the model
model = cp_model.CpModel()

# Create variables
schedule = {}
for dept, subs in subjects.items():
    for sem in semesters:
        for sub in subs:
            for room in rooms['BlockA'] + rooms['BlockB']:
                for time in class_times:
                    schedule[(dept, sem, sub, room, time)] = model.NewBoolVar(f"{dept}_{sem}_{sub}_{room}_{time}")

# Constraints
# 1. No overlapping classes for the same department and semester
for dept, subs in departments.items():
    for sem in semesters:
        for time in class_times:
            model.AddAtMostOne(schedule[(dept, sem, sub, room, time)] 
                              for sub in subjects[dept] 
                              for room in rooms['BlockA'] + rooms['BlockB'])

# 2. Room capacity constraints
# (This requires knowing the number of students per class, which isn't provided in the sample data)
# Placeholder: Ensure only one class per room per time slot
for room in rooms['BlockA'] + rooms['BlockB']:
    for time in class_times:
        model.AddAtMostOne(schedule[(dept, sem, sub, room, time)] 
                          for dept in departments 
                          for sem in semesters 
                          for sub in subjects[dept])

# 3. Breathing gap constraints
# Implemented by ensuring that if a class is scheduled at a certain time, 
# the next time slot is available (this is a simplified version)
for dept, subs in departments.items():
    for sem in semesters:
        for sub in subjects[dept]:
            for room in rooms['BlockA'] + rooms['BlockB']:
                for i in range(len(class_times) - 1):
                    current_time = class_times[i]
                    next_time = class_times[i + 1]
                    model.Add(schedule[(dept, sem, sub, room, next_time)] <= 1 - schedule[(dept, sem, sub, room, current_time)])

# 4. Proximity constraints
# Simplified: Limit the number of different blocks used by a department in a semester
for dept, subs in departments.items():
    for sem in semesters:
        blocks_used = []
        for sub in subjects[dept]:
            for room in rooms['BlockA'] + rooms['BlockB']:
                block = 'A' if room in rooms['BlockA'] else 'B'
                blocks_used.append(block)
        # Ensure no more than 2 blocks are used
        model.Add(sum(block == 'A' for block in blocks_used) <= 2)
        model.Add(sum(block == 'B' for block in blocks_used) <= 2)

# 5. Department room allocation constraints
# Ensure classes are scheduled within the allocated rooms for each department
# (Assuming departments have specific blocks; adjust as needed)
department_blocks = {
    'CSE': ['BlockA'],
    'EC': ['BlockA'],
    'ICT': ['BlockA'],
    'Petroleum': ['BlockB'],
    'Mechanical': ['BlockB'],
    'Arts': ['BlockB'],
    'Science': ['BlockB']
}

for dept, subs in subjects.items():
    for sem in semesters:
        for sub in subs:
            for room in rooms['BlockA'] + rooms['BlockB']:
                if room not in rooms[department_blocks[dept][0]]:
                    for time in class_times:
                        model.Add(schedule[(dept, sem, sub, room, time)] == 0)

# Objective (optional): For example, minimize the total number of gaps
# Here, no specific objective is set; it's a feasibility problem

# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    for key, var in schedule.items():
        if solver.Value(var) == 1:
            print(f"{key[0]} - {key[1]} - {key[2]} in {key[3]} at {key[4]}")
else:
    print("No solution found.")
