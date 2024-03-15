import pytest
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from create import Base, User, FitnessGoal, Workout, NutritionLog, SleepRecord, MoodLog  # Ensure this import matches your model file's actual name and path.

@pytest.fixture(scope="session") # This fixture will be shared across all tests in the session
def engine():
    '''Create a clean database for the tests.'''
    return create_engine("sqlite:///:memory:") # Using an in-memory database for testing

@pytest.fixture(scope="session") 
def tables(engine):
    '''Create the tables in the database.'''
    Base.metadata.create_all(engine) 
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    '''Create a new session for each test. Rollback changes after each test.'''
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)
    yield Session()
    Session.remove()
    transaction.rollback()
    connection.close()

# Test User Model
def test_user_model(session):
    '''Test the User model.'''
    user = User(name="John Doe", age=30, gender="Male", weight=80.5, height=180.3, email="johndoe@example.com", bio="A passionate runner.")
    session.add(user)
    session.commit()

    # Test Insertion
    inserted_user = session.query(User).first()
    assert inserted_user.name == "John Doe"

    # Test Relationships
    goal = FitnessGoal(goal="Marathon", description="Run a full marathon.", user_id=user.id)
    session.add(goal)
    session.commit()
    assert len(user.fitness_goals) == 1

# Test FitnessGoal Model
def test_fitness_goal_model(session):
    '''Test the FitnessGoal model.'''
    user = User(name="Alice Wonderland", age=28, gender="Female", weight=60, height=165, email="alice@example.com", bio="Yoga enthusiast.")
    session.add(user)
    session.commit()

    goal = FitnessGoal(goal="Yoga Master", description="Achieve the advanced yoga poses.", user_id=user.id, target_date=date(2024, 12, 31), completed=False)
    session.add(goal)
    session.commit()

    # Test Relationship
    assert goal.user.name == "Alice Wonderland"

# Test Workout Model
def test_workout_model(session):
    '''Test the Workout model.'''
    user = User(name="Bob Builder", age=35, gender="Male", weight=90, height=175, email="bobb@example.com", bio="Gym junkie.")
    session.add(user)
    session.commit()

    workout = Workout(date=date.today(), duration=60, type="Weightlifting", intensity="High", calories_burned=500, user_id=user.id)
    session.add(workout)
    session.commit()

    # Test Insertion and Relationship
    assert len(user.workouts) > 0
    assert user.workouts[0].type == "Weightlifting"

def test_nutrition_log_model(session):
    '''Test the NutritionLog model.'''
    user = User(name="Cathy Vegan", age=27, gender="Female", weight=55, height=165, email="cathyv@example.com", bio="Vegan and nutrition enthusiast.")
    session.add(user)
    session.commit()

    nutrition_log = NutritionLog(date=date.today(), meal_type="Breakfast", calories=350, proteins=15, carbs=50, fats=10, user_id=user.id)
    session.add(nutrition_log)
    session.commit()

    # Test Insertion and Relationship
    assert len(user.nutrition_logs) == 1
    assert user.nutrition_logs[0].meal_type == "Breakfast"

def test_sleep_record_model(session):
    '''Test the SleepRecord model.'''
    user = User(name="Danny Dreamer", age=34, gender="Male", weight=70, height=175, email="dannyd@example.com", bio="Exploring the world of dreams.")
    session.add(user)
    session.commit()

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=8)  # Assuming 8 hours of sleep
    sleep_record = SleepRecord(start_time=start_time, end_time=end_time, quality="Good", deep_sleep_duration=3.5, user_id=user.id)
    session.add(sleep_record)
    session.commit()

    # Test Insertion and Relationship
    assert len(user.sleep_records) == 1
    assert user.sleep_records[0].quality == "Good"

def test_mood_log_model(session):
    '''Test the MoodLog model.'''
    user = User(name="Eva Emotion", age=29, gender="Female", weight=60, height=170, email="evae@example.com", bio="On a journey to emotional wellness.")
    session.add(user)
    session.commit()

    mood_log = MoodLog(date=date.today(), mood="Happy", stress_level=3, user_id=user.id)
    session.add(mood_log)
    session.commit()

    # Test Insertion and Relationship
    assert len(user.mood_logs) == 1
    assert user.mood_logs[0].mood == "Happy"


if __name__ == "__main__":
    pytest.main()
