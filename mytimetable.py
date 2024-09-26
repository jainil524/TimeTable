from datetime import datetime, timedelta
import json
from Lecture import Lecture

def time_to_minutes(t):
    return int(t.split(":")[0]) * 60 + int(t.split(":")[1])

def minutes_to_time(m):
    return f"{m // 60:02d}:{m % 60:02d}"

def load_config():
    with open("class.config.json") as f:
        class_config = json.load(f)
    with open("break.config.json") as f:
        break_config = json.load(f)
    return class_config, break_config

def parse_break_times(break_config):
    breaks = []
    for break_type in break_config["Breaks"]:
        for timing in break_config["Breaks"][break_type]["timeing"]:
            start_time, end_time = timing.split("-")
            breaks.append((time_to_minutes(start_time), time_to_minutes(end_time)))
    return breaks

def create_schedule(lectures, class_config, break_config):
    schedule = {day: [] for day in class_config["DAYS"]}
    class_start_time = time_to_minutes(class_config["START_TIME"])
    class_end_time = time_to_minutes(class_config["END_TIME"])
    lecture_duration = class_config["LECTURE_DURATION"]
    lab_duration = class_config["LAB_DURATION"]
    max_lectures_per_day = class_config["MAX_LECTURES_PER_DAY"]
    max_same_lecture_count_per_day = class_config["MAX_LECTURES_PER_DAY"]
    gap_between_lectures = break_config["GAP_TIME_BETWEEN_LECTURES"]
    breaks = parse_break_times(break_config)

    days = class_config["DAYS"]
    current_day_index = days.index(class_config["WEEK_START_DAY"])
    
    def is_time_available(start_time, end_time, day_schedule):
        for lecture in day_schedule:
            lec_start, lec_end = map(time_to_minutes, lecture["Time"].split("-"))
            if not (end_time <= lec_start or start_time >= lec_end):
                return False
        return True
    
    def add_lecture(day, course_name, professor_name, start_time, end_time):
        schedule[day].append({
            "Course Name": course_name,
            "Time": f"{minutes_to_time(start_time)}-{minutes_to_time(end_time)}",
            "Professor Name": professor_name,
            "Corp": course_name
        })
    
    for lecture in lectures:
        course_name = lecture.course_name
        professor_name = lecture.professor
        duration = lecture_duration  # convert hours to minutes
        total_lectures = lecture.hpw

        while total_lectures > 0:
            day = days[current_day_index]
            current_time = class_start_time
            lectures_today = 0
            same_lecture_count = 0

            while lectures_today < max_lectures_per_day and total_lectures > 0:
                if any(start <= current_time <= end for start, end in breaks):
                    current_time = max(end for start, end in breaks if start <= current_time)
                elif is_time_available(current_time, current_time + lecture_duration, schedule[day]):
                    end_time = current_time + lecture_duration
                    add_lecture(day, course_name, professor_name, current_time, end_time)
                    current_time = end_time + gap_between_lectures
                    lectures_today += 1
                    same_lecture_count += 1
                    total_lectures -= 1
                else:
                    current_time += 5  # skip to next possible time slot if overlap occurs

                if current_time >= class_end_time:
                    break

            current_day_index = (current_day_index + 1) % len(days)

    return schedule

def print_schedule(schedule):
    for day, lectures in schedule.items():
        lectures = sorted(
            lectures, key=lambda x: time_to_minutes(x["Time"].split("-")[0])
        )
        print(f"\n{day}")
        print("=" * 40)
        for lecture in lectures:
            print(f"Course Name: {lecture['Course Name']}")
            print(f"Time: {lecture['Time']}")
            print(f"Professor Name: {lecture['Professor Name']}")
            print(f"Corp: {lecture['Corp']}")
            print("-" * 40)

if __name__ == "__main__":
    class_config, break_config = load_config()
    lectures = [
        Lecture(name="Introduction to Programming", corp="Dr. Shaun Murphy",  credit=3, professor="Dr. Neil Melendez" ,hpw=3),
        Lecture(name="Data Structures", corp="Dr. Clair Brown", credit=4, professor="Dr. Glassman Aaron"  ,hpw=4),
        Lecture(name="Algorithms", corp="Dr. Neil Melendez", credit=4, professor="Dr. Andrews Marcus"  ,hpw=4),
        Lecture(name="Database Systems", corp="Dr. Lim Audrey", credit=4, professor="Dr. Kalu Jared"  ,hpw=4),
        Lecture(name="Operating Systems", corp="Dr. Kalu Jared", credit=4, professor="Dr. Park Alex"  ,hpw=4),
        Lecture(name="Computer Networks", corp="Dr. Andrews Marcus", credit=3, professor="Dr. Lim Audrey"  ,hpw=3),
        Lecture(name="Software Engineering", corp="Dr. Glassman Aaron", credit=4, professor="Dr. Shaun Murphy"  ,hpw=4),
        Lecture(name="Artificial Intelligence", corp="Dr. Park Alex", credit=4, professor="Dr. Clair Brown"  ,hpw=4),
    ]
    schedule = create_schedule(lectures, class_config, break_config)
    print_schedule(schedule)
