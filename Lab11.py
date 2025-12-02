import os
import math
import matplotlib.pyplot as plt

# ... (keep load_students, load_assignments, load_submissions,
# calculate_student_grade, assignment_stats, main, etc. unchanged)
# I'll include the full file below; only the histogram function/appearance changed.

# --------------------------
# OPTION 3 — HISTOGRAM (refined to match screenshot)
# --------------------------
def show_histogram(name, assignments_by_name, submissions):
    normalized = name.lower()

    if normalized not in assignments_by_name:
        return False

    assignment_id, _ = assignments_by_name[normalized]

    if assignment_id not in submissions:
        return False

    scores = [p for (_, p) in submissions[assignment_id]]
    if not scores:
        return False

    # Create figure with size similar to example screenshot
    plt.figure(figsize=(8.5, 5.5))

    # Use a moderate number of bins for a smooth bell-curve look
    bins = 8
    counts, bin_edges, patches = plt.hist(scores, bins=bins, edgecolor='black', linewidth=0.6)

    ax = plt.gca()

    # Set x-range to focus on scores area (matches screenshot)
    plt.xlim(50, 100)

    # Ensure y-axis starts at 0 and add small headroom
    top = math.ceil(max(counts)) if len(counts) > 0 else 1
    plt.ylim(0, top + 1)

    # Title and labels
    plt.title(name)
    plt.xlabel("Score Percent")
    plt.ylabel("Number of Students")

    # Make a clean black border similar to the screenshot
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.0)
        spine.set_color("black")

    # Turn on only left and bottom ticks if you want that look,
    # but keep the outer box — screenshot shows ticks on left/bottom only.
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # Tweak tick label sizes (optional)
    ax.tick_params(axis='both', which='major', labelsize=10)

    plt.tight_layout()
    plt.show()
    return True


# --------------------------
# FULL FILE (everything together)
# --------------------------
def load_students(path="data/students.txt"):
    students_by_name = {}
    students_by_id = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id = line[:3]
            student_name = line[3:].strip()
            students_by_name[student_name.lower()] = student_id
            students_by_id[student_id] = student_name
    return students_by_name, students_by_id

def load_assignments(path="data/assignments.txt"):
    assignments_by_name = {}
    assignments_by_id = {}
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        assignment_id = lines[i + 1]
        points = int(lines[i + 2])
        assignments_by_name[name.lower()] = (assignment_id, points)
        assignments_by_id[assignment_id] = (name, points)
    return assignments_by_name, assignments_by_id

def load_submissions(path="data/submissions"):
    submissions = {}
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if not os.path.isfile(file_path):
            continue
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    continue
                student_id, assignment_id, percent_str = parts
                try:
                    percent = float(percent_str)
                except:
                    continue
                submissions.setdefault(assignment_id, []).append((student_id, percent))
    return submissions

def calculate_student_grade(name, students_by_name, assignments_by_id, submissions):
    normalized = name.lower()
    if normalized not in students_by_name:
        return None
    student_id = students_by_name[normalized]
    total_earned = 0
    total_points = 0
    for assignment_id, (assignment_name, points) in assignments_by_id.items():
        for sid, percent in submissions.get(assignment_id, []):
            if sid == student_id:
                total_earned += (percent / 100) * points
                total_points += points
    if total_points == 0:
        return 0
    return round((total_earned / total_points) * 100)

def assignment_stats(name, assignments_by_name, submissions):
    normalized = name.lower()
    if normalized not in assignments_by_name:
        return None
    assignment_id, _ = assignments_by_name[normalized]
    if assignment_id not in submissions:
        return None
    percents = [p for (_, p) in submissions[assignment_id]]
    mn = round(min(percents))
    avg = math.floor(sum(percents) / len(percents))
    mx = round(max(percents))
    return mn, avg, mx

def main():
    students_by_name, students_by_id = load_students()
    assignments_by_name, assignments_by_id = load_assignments()
    submissions = load_submissions()
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")
    choice = input("Enter your selection: ").strip()
    if choice == "1":
        name = input("What is the student's name: ").strip()
        result = calculate_student_grade(name, students_by_name, assignments_by_id, submissions)
        if result is None:
            print("Student not found")
        else:
            print(f"{result}%")
    elif choice == "2":
        name = input("What is the assignment name: ").strip()
        result = assignment_stats(name, assignments_by_name, submissions)
        if result is None:
            print("Assignment not found")
        else:
            mn, avg, mx = result
            print(f"Min: {mn}%")
            print(f"Avg: {avg}%")
            print(f"Max: {mx}%")
    elif choice == "3":
        name = input("What is the assignment name: ").strip()
        ok = show_histogram(name, assignments_by_name, submissions)
        if not ok:
            print("Assignment not found")

if __name__ == "__main__":
    main()









