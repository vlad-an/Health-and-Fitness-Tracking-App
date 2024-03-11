from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord, MoodLog
from faker import Faker
import random
from datetime import datetime, timedelta

engine = create_engine('sqlite:///health_fitness_app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
faker = Faker()

def create_sample_users():
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

def create_sample_fitness_goals():
    users = session.query(User).all()
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

def create_sample_workouts():
    users = session.query(User).all()
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

def create_sample_nutrition_logs():
    users = session.query(User).all()
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

def create_sample_sleep_records():
    users = session.query(User).all()
    for user in users:
        for _ in range(10):  # 10 days of sleep records for extended data
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

def create_sample_mood_logs():
    users = session.query(User).all()
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

if __name__ == '__main__':
    create_sample_users()
    create_sample_fitness_goals()
    create_sample_workouts()
    create_sample_nutrition_logs()
    create_sample_sleep_records()
    create_sample_mood_logs()
