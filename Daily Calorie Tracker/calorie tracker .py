print("---------------------------------------------------------------\n")
print("\n Welcome to DailyCal Tracker!")
print("Log your meals, count your calories, and take control of your health! 💪")
print("Let's start tracking your nutrition and stay healthy!")
print("---------------------------------------------------------------\n")

Meal_Name = []
Meal_set = set()  # To prevent duplicates
Cal_Intake = []
result = ""  # Limit result
User_Info = {}  # store final data

N_User = input("Enter your Name: ")  # getting  the name of the user 
calorie_goal = float(input("Enter your max amount of cal you want to maintain: "))
N_meals = int(input("How many meals are you having today: "))  # Checking how many meals the users wants to add today ?

for i in range(N_meals):
    print("\n")
    M_name = input(f"Enter your {i+1} meal name: ")

    # Prevent duplicate meal entries
    if M_name in Meal_set:
        print("⚠️ You already entered this meal! Skipping duplicate...")
        continue

    cal = float(input("Enter the amount of calorie you get: "))
    Meal_set.add(M_name)
    Meal_Name.append(M_name)
    Cal_Intake.append(cal)

# Calculate total calories
total_cal = sum(Cal_Intake)

if total_cal == calorie_goal:
    print(f"\n Congratulations {N_User}, you maintained your calorie intake perfectly!")
    result = "Maintained"
elif total_cal < calorie_goal:
    print(f"\n Your calorie intake is less by {calorie_goal - total_cal:.2f} kcal.")
    result = f"Less by {calorie_goal - total_cal:.2f} kcal"
else:
    print(f"\n You exceeded your calorie goal by {total_cal - calorie_goal:.2f} kcal.")
    result = f"Exceeded by {total_cal - calorie_goal:.2f} kcal"

# Display results
print("\n====================================")
print("\n 📝 Summary of Your Meals:\n")
print("Meal Name\t\tCalories")
print("-" * 35)

# Print each meal in tabular form.
for meal, cal in zip(Meal_Name, Cal_Intake):
    print(f"{meal:<16}\t{cal:.2f}")

print("-" * 35)
print(f"Total:\t\t\t{total_cal:.2f}")
print(f"Average:\t\t{total_cal / len(Cal_Intake):.2f}")
print(f"Status:\t\t\t{result}")
print("====================================\n")
print("💬 Thanks for using DailyCal Tracker! Stay healthy and balanced! \n")