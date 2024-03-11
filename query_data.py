from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord
from datetime import datetime, timedelta

# Establish a connection to the database
engine = create_engine('sqlite:///health_fitness_app.db')
Session = sessionmaker(bind=engine)
session = Session()

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
