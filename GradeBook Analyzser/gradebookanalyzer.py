import csv
import statistics

# -------------------------------
# Function to load marks manually
# -------------------------------
def manual_entry():
    marks = []
    n = int(input("Enter number of students: "))
    for i in range(n):
        mark = float(input(f"Enter mark for student {i+1}: "))
        marks.append(mark)
    return marks

# -------------------------------
# Function to load marks from CSV
# -------------------------------
def load_from_csv(filename):
    marks = []
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Avoid empty rows
                    marks.append(float(row[0]))
        return marks
    except FileNotFoundError:
        print("CSV file not found!")
        return []

# -------------------------------
# Calculate statistics
# -------------------------------
def calculate_stats(marks):
    avg = sum(marks) / len(marks)
    med = statistics.median(marks)
    highest = max(marks)
    lowest = min(marks)
    return avg, med, highest, lowest

# -------------------------------
# Assign grades
# -------------------------------
def assign_grades(marks):
    grade_dict = {}
    for mark in marks:
        if mark >= 90:
            grade = "A"
        elif mark >= 80:
            grade = "B"
        elif mark >= 70:
            grade = "C"
        elif mark >= 60:
            grade = "D"
        else:
            grade = "F"
        grade_dict[mark] = grade
    return grade_dict

# -------------------------------
# Count grade distribution
# -------------------------------
def grade_distribution(grade_dict):
    distribution = {"A":0, "B":0, "C":0, "D":0, "F":0}
    for grade in grade_dict.values():
        distribution[grade] += 1
    return distribution

# -------------------------------
# Display results in table format
# -------------------------------
def display_results(marks, grade_dict, stats, distribution):
    avg, med, highest, lowest = stats

    print("\n--- GradeBook Analysis ---")
    print(f"{'Mark':<10}{'Grade'}")
    print("-" * 20)
    for mark, grade in grade_dict.items():
        print(f"{mark:<10}{grade}")
    
    print("\n--- Statistics ---")
    print(f"Average Score : {avg:.2f}")
    print(f"Median Score  : {med:.2f}")
    print(f"Highest Score : {highest}")
    print(f"Lowest Score  : {lowest}")

    print("\n--- Grade Distribution ---")
    for grade, count in distribution.items():
        print(f"{grade}: {count}")

    # List comprehension for pass/fail
    passed = [m for m in marks if m >= 40]
    failed = [m for m in marks if m < 40]

    print("\n--- Pass/Fail Summary (Using List Comprehension) ---")
    print(f"Passed Students: {len(passed)} → {passed}")
    print(f"Failed Students: {len(failed)} → {failed}")


# -------------------------------
# Main Menu Loop
# -------------------------------
def main():
    while True:
        print("\n===== GradeBook Analyzer =====")
        print("1. Enter marks manually")
        print("2. Load marks from CSV")
        print("3. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            marks = manual_entry()

        elif choice == "2":
            filename = input("Enter CSV filename (e.g., marks.csv): ")
            marks = load_from_csv(filename)
            if not marks:
                continue

        elif choice == "3":
            print("Exiting GradeBook Analyzer…")
            break

        else:
            print("Invalid choice! Try again.")
            continue
        
        # Perform calculations
        stats = calculate_stats(marks)
        grade_dict = assign_grades(marks)
        distribution = grade_distribution(grade_dict)

        # Display results
        display_results(marks, grade_dict, stats, distribution)


# Run the program
main()
