from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord
from faker import Faker
import random
from datetime import datetime, timedelta

engine = create_engine('sqlite:///health_fitness_app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
faker = Faker()

def create_sample_users():
    for _ in range(10):  # Creating 10 sample users
        user = User(
            name=faker.name(),
            age=random.randint(18, 65),
            gender=random.choice(['Male', 'Female']),
            weight=random.uniform(50.0, 100.0),
            height=random.uniform(150.0, 200.0)
        )
        session.add(user)
    session.commit()

def create_sample_fitness_goals():
    users = session.query(User).all()
    for user in users:
        goal = FitnessGoal(
            goal=random.choice(['Lose weight', 'Gain muscle', 'Improve stamina', 'Increase flexibility']),
            target_date=datetime.now() + timedelta(days=random.randint(30, 365)),
            user_id=user.id
        )
        session.add(goal)
    session.commit()

def create_sample_workouts():
    users = session.query(User).all()
    for user in users:
        for _ in range(5):  # 5 workouts per user
            workout = Workout(
                date=faker.date_between(start_date='-1y', end_date='today'),
                duration=random.choice([30, 45, 60, 75, 90]),
                type=random.choice(['Running', 'Cycling', 'Swimming', 'Yoga', 'Gym', 'Hiking']),
                intensity=random.choice(['Low', 'Medium', 'High']),
                user_id=user.id
            )
            session.add(workout)
    session.commit()

def create_sample_nutrition_logs():
    users = session.query(User).all()
    for user in users:
        for _ in range(7):  # 7 days of nutrition logs
            nutrition_log = NutritionLog(
                date=faker.date_between(start_date='-1w', end_date='today'),
                meal_type=random.choice(['Breakfast', 'Lunch', 'Dinner', 'Snack']),
                calories=random.randint(200, 800),
                user_id=user.id
            )
            session.add(nutrition_log)
    session.commit()

def create_sample_sleep_records():
    users = session.query(User).all()
    for user in users:
        for _ in range(7):  # 7 days of sleep records
            start_time = datetime.now() - timedelta(days=random.randint(1, 7))
            end_time = start_time + timedelta(hours=random.randint(6, 9))
            sleep_record = SleepRecord(
                start_time=start_time,
                end_time=end_time,
                quality=random.choice(['Poor', 'Fair', 'Good', 'Excellent']),
                user_id=user.id
            )
            session.add(sleep_record)
    session.commit()

if __name__ == '__main__':
    create_sample_users()
    create_sample_fitness_goals()
    create_sample_workouts()
    create_sample_nutrition_logs()
    create_sample_sleep_records()
