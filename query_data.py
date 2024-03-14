from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord, MoodLog
from datetime import datetime, timedelta

# Establish a connection to the database
engine = create_engine('sqlite:///health_fitness_app.db') # Create an engine that connects to the database
Session = sessionmaker(bind=engine) # Create a session to interact with the database
session = Session() # Create an instance of the session

def get_user_workouts(user_id):
    """Retrieve all workouts for a specific user"""
    workouts = session.query(Workout).filter(Workout.user_id == user_id).all()
    for workout in workouts:
        print(f"Workout ID: {workout.id}, Type: {workout.type}, Duration: {workout.duration} minutes, Date: {workout.date}")

def get_average_sleep_duration(user_id):
    """Calculate the average sleep duration for a user over the last month"""
    one_month_ago = datetime.now() - timedelta(days=30)
    average_duration = session.query(func.avg(func.julianday(SleepRecord.end_time) - func.julianday(SleepRecord.start_time)) * 24).\
        filter(SleepRecord.user_id == user_id, SleepRecord.start_time >= one_month_ago).scalar()
    print(f"Average Sleep Duration (hours) for the last month: {average_duration:.2f}")

def get_nutrition_summary(user_id, date):
    """Summarize nutrition for a specific day"""
    logs = session.query(NutritionLog).filter(NutritionLog.user_id == user_id, func.date(NutritionLog.date) == date).all()
    total_calories = 0
    for log in logs:
        total_calories += log.calories
        print(f"Meal: {log.meal_type}, Calories: {log.calories}")
    print(f"Total Calories for {date}: {total_calories}")

def get_user_fitness_goals(user_id):
    """List all fitness goals for a user"""
    goals = session.query(FitnessGoal).filter(FitnessGoal.user_id == user_id).all()
    for goal in goals:
        print(f"Goal: {goal.goal}, Target Date: {goal.target_date}")

def get_detailed_nutrition_summary(user_id, start_date, end_date):
    """Provide a detailed summary of nutrition between specified dates"""
    logs = session.query(NutritionLog).filter(NutritionLog.user_id == user_id, NutritionLog.date.between(start_date, end_date)).all()
    total_calories, total_proteins, total_carbs, total_fats = 0, 0, 0, 0
    for log in logs:
        total_calories += log.calories
        total_proteins += log.proteins
        total_carbs += log.carbs
        total_fats += log.fats
    print(f"Nutrition Summary from {start_date} to {end_date}:")
    print(f"Total Calories: {total_calories}, Proteins: {total_proteins}g, Carbs: {total_carbs}g, Fats: {total_fats}g")

def get_monthly_workout_summary(user_id, current_month, current_year):
    """Monthly summary of workouts including total duration and average intensity"""
    workouts = session.query(Workout).filter(Workout.user_id == user_id, func.extract('month', Workout.date) == current_month, func.extract('year', Workout.date) == current_year).all()
    total_duration = sum([workout.duration for workout in workouts])
    average_intensity = {workout.intensity for workout in workouts}
    print(f"Total Workout Duration this Month: {total_duration} minutes")
    print(f"Workout Intensities Encountered: {', '.join(average_intensity)}")

def get_sleep_quality_overview(user_id):
    """Overview of sleep quality distribution over the last month"""
    one_month_ago = datetime.now() - timedelta(days=30)
    sleep_records = session.query(SleepRecord).filter(SleepRecord.user_id == user_id, SleepRecord.start_time >= one_month_ago).all()
    quality_counts = {"Poor": 0, "Fair": 0, "Good": 0, "Excellent": 0}
    for record in sleep_records:
        quality_counts[record.quality] += 1
    print("Sleep Quality Overview:")
    for quality, count in quality_counts.items():
        print(f"{quality}: {count} nights")

def get_user_mood_trends(user_id):
    """Analyze mood trends for a user over the last month"""
    one_month_ago = datetime.now() - timedelta(days=30)
    mood_logs = session.query(MoodLog).filter(MoodLog.user_id == user_id, MoodLog.date >= one_month_ago).all()
    mood_counts = {}
    for log in mood_logs:
        mood_counts[log.mood] = mood_counts.get(log.mood, 0) + 1
    print("Mood Trends Over the Last Month:")
    for mood, count in mood_counts.items():
        print(f"{mood}: {count} days")

def get_progress_towards_fitness_goals(user_id):
    """Track progress towards fitness goals"""
    goals = session.query(FitnessGoal).filter(FitnessGoal.user_id == user_id).all()
    for goal in goals:
        status = "Completed" if goal.completed else "In Progress"
        print(f"Goal: {goal.goal}, Status: {status}, Target Date: {goal.target_date}")

if __name__ == '__main__':
    user_id = 1  # Example user ID
    print("User Workouts:")
    get_user_workouts(user_id)
    
    print("\nAverage Sleep Duration:")
    get_average_sleep_duration(user_id)
    
    date = "2024-03-04"  # Example date
    print(f"\nNutrition Summary for {date}:")
    get_nutrition_summary(user_id, date)
    
    print("\nUser Fitness Goals:")
    get_user_fitness_goals(user_id)

    start_date, end_date = "2024-03-04", "2024-03-28"  # Sample date range
    print("\nDetailed Nutrition Summary:")
    get_detailed_nutrition_summary(user_id, start_date, end_date)

    print("\nMonthly Workout Summary:")
    get_monthly_workout_summary(user_id, 7, 2023)

    print("\nSleep Quality Overview:")
    get_sleep_quality_overview(user_id)

    print("\nUser Mood Trends:")
    get_user_mood_trends(user_id)

    print("\nProgress Towards Fitness Goals:")
    get_progress_towards_fitness_goals(user_id)
