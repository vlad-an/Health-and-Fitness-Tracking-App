from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord, MoodLog
from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError


engine = create_engine('sqlite:///health_fitness_app.db') # Create an engine that connects to the database
Base.metadata.bind = engine # Bind the engine to the metadata of the Base class to reflect the tables

DBSession = sessionmaker(bind=engine) # Create a session to interact with the database
session = DBSession() # Create an instance of the session
faker = Faker() # Create an instance of the Faker class to generate fake data

def create_sample_users():
    '''Create sample users to populate the database'''
    for _ in range(20):  # Creating 20 sample users to enrich the dataset
        user = User(
            name=faker.name(),
            age=random.randint(18, 65),
            gender=random.choice(['Male', 'Female', 'Other']),
            weight=random.uniform(50.0, 120.0),
            height=random.uniform(150.0, 210.0),
            email=faker.email(),
            bio=faker.text(max_nb_chars=200)
        )
        session.add(user)
    session.commit()
    return session.query(User).all()

def create_sample_fitness_goals(users):
    '''Create sample fitness goals for the users in the database'''
    for user in users:
        for _ in range(random.randint(1, 3)):  # Multiple fitness goals per user
            goal = FitnessGoal(
                user_id=user.id,
                goal=faker.sentence(nb_words=6),
                description=faker.text(max_nb_chars=200),
                target_date=datetime.now() + timedelta(days=random.randint(30, 365)),
                completed=random.choice([True, False])
            )
            session.add(goal)
    session.commit()

def create_sample_workouts(users):
    '''Create sample workout history for the users in the database'''
    for user in users:
        for _ in range(random.randint(5, 15)):  # More diverse workout history
            workout = Workout(
                user_id=user.id,
                date=faker.date_between(start_date='-1y', end_date='today'),
                duration=random.choice([30, 45, 60, 75, 90, 120]),
                type=random.choice(['Running', 'Cycling', 'Swimming', 'Yoga', 'Gym', 'Hiking', 'Dancing', 'CrossFit']),
                intensity=random.choice(['Low', 'Medium', 'High']),
                calories_burned=random.randint(100, 800),
                notes=faker.text(max_nb_chars=100)
            )
            session.add(workout)
    session.commit()

def create_sample_nutrition_logs(users):
    '''Create sample nutrition logs for the users in the database'''
    for user in users:
        for _ in range(14):  # Extending to two weeks of nutrition logs for more data
            nutrition_log = NutritionLog(
                user_id=user.id,
                date=faker.date_between(start_date='-2w', end_date='today'),
                meal_type=random.choice(['Breakfast', 'Lunch', 'Dinner', 'Snack']),
                calories=random.randint(100, 1200),
                proteins=random.uniform(0, 100),
                carbs=random.uniform(0, 300),
                fats=random.uniform(0, 100),
                notes=faker.text(max_nb_chars=100)
            )
            session.add(nutrition_log)
    session.commit()

def create_sample_sleep_records(users):
    '''Create sample sleep records for the users in the database'''
    for user in users:
        for _ in range(10):  # 10 days of sleep records 
            start_time = datetime.now() - timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(hours=random.randint(6, 12))
            sleep_record = SleepRecord(
                user_id=user.id,
                start_time=start_time,
                end_time=end_time,
                quality=random.choice(['Poor', 'Fair', 'Good', 'Excellent']),
                deep_sleep_duration=random.uniform(1, 5),
                notes=faker.text(max_nb_chars=100)
            )
            session.add(sleep_record)
    session.commit()

def create_sample_mood_logs(users):
    '''Create sample mood logs for the users in the database'''
    for user in users:
        for _ in range(10):  # 10 days of mood logs to understand emotional well-being
            mood_log = MoodLog(
                user_id=user.id,
                date=faker.date_between(start_date='-1m', end_date='today'),
                mood=random.choice(['Happy', 'Sad', 'Angry', 'Stressed', 'Calm', 'Anxious']),
                stress_level=random.randint(1, 10),
                notes=faker.text(max_nb_chars=200)
            )
            session.add(mood_log)
    session.commit()

def register_user_with_goals(user_details, goal_details):
    '''Register a new user with fitness goals and return the user's ID for further operations'''
    try:
        new_user = User(**user_details)  # Assuming user_details is a dict with user info
        session.add(new_user)
        session.flush()  # This is to obtain the new user's ID if needed for related operations

        for goal_detail in goal_details:
            goal_detail['user_id'] = new_user.id
            new_goal = FitnessGoal(**goal_detail)
            session.add(new_goal)
        
        session.commit()
        print("User and goals successfully created.")
        return new_user.id  # Returning the new user's ID for further use
    except SQLAlchemyError as e:
        session.rollback() # Rollback the changes in case of an error
        print(f"Error during registration: {e}")
        return None

def log_workout_and_update_goals(user_id, workout_data, goal_updates):
    '''Log a new workout and update the status of fitness goals for the user'''
    try:
        new_workout = Workout(user_id=user_id, **workout_data) # Assuming workout_data is a dict with workout info
        session.add(new_workout) # Log the new workout

        for goal_id, completed in goal_updates.items(): # Update the status of fitness goals
            goal = session.query(FitnessGoal).filter_by(id=goal_id, user_id=user_id).first()
            if goal:
                goal.completed = completed
        
        session.commit()
        print("Workout logged and goals updated successfully.")
    except SQLAlchemyError as e:
        session.rollback() # Rollback the changes in case of an error
        print(f"Error during workout logging: {e}")

if __name__ == '__main__':
    users = create_sample_users()
    create_sample_fitness_goals(users)
    create_sample_workouts(users)
    create_sample_nutrition_logs(users)
    create_sample_sleep_records(users)
    create_sample_mood_logs(users)
    
    user_details = { # Example user details
        'name': faker.name(), 
        'age': random.randint(18, 65),
        'gender': random.choice(['Male', 'Female', 'Other']),
        'weight': random.uniform(50.0, 120.0),
        'height': random.uniform(150.0, 210.0),
        'email': faker.email(),
        'bio': faker.text(max_nb_chars=200)
    }

    goal_details = [{ # Example fitness goal details
        'goal': faker.sentence(nb_words=6),
        'description': faker.text(max_nb_chars=200),
        'target_date': datetime.now() + timedelta(days=random.randint(30, 365)),
        'completed': False
    }]

    new_user_id = register_user_with_goals(user_details, goal_details) # Register a new user with fitness goals
    if new_user_id:
        workout_data = {
            'date': datetime.now(),
            'duration': 60,
            'type': 'Running',
            'intensity': 'High',
            'calories_burned': 500,
            'notes': 'Felt great!',
        }
        
        goal_updates = {1: True}  # Example goal update (goal ID: completed status)
        log_workout_and_update_goals(new_user_id, workout_data, goal_updates)
