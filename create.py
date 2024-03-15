from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base() # Base class for our classes to inherit from

class User(Base):
    '''This class represents the user table in the database'''
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True) # Unique identifier for each user
    name = Column(String, nullable=False) # Name of the user
    age = Column(Integer) # Age of the user
    gender = Column(String) # Gender of the user
    weight = Column(Float) # Weight of the user in kilograms
    height = Column(Float) # Height of the user in centimeters
    email = Column(String, unique=True, nullable=False,index=True) # Email address of the user
    bio = Column(Text) # A short bio of the user
    fitness_goals = relationship("FitnessGoal", back_populates="user", cascade="all, delete, delete-orphan") # Relationship with the FitnessGoal class (one-to-many)
    workouts = relationship("Workout", back_populates="user", cascade="all, delete, delete-orphan") # Relationship with the Workout class (one-to-many)
    nutrition_logs = relationship("NutritionLog", back_populates="user", cascade="all, delete, delete-orphan") # Relationship with the NutritionLog class (one-to-many)
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete, delete-orphan") # Relationship with the SleepRecord class (one-to-many)
    mood_logs = relationship("MoodLog", back_populates="user", cascade="all, delete, delete-orphan") # Relationship with the MoodLog class (one-to-many)

class FitnessGoal(Base):
    '''This class represents the fitness_goals table in the database'''
    __tablename__ = 'fitness_goals'
    id = Column(Integer, primary_key=True) # Unique identifier for each fitness goal
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign key to link the fitness goal to a user
    goal = Column(String, nullable=False) # The fitness goal
    description = Column(Text) # A detailed description of the goal
    target_date = Column(Date) # The target date to achieve the goal
    completed = Column(Boolean, default=False) # Whether the goal has been completed or not
    user = relationship("User", back_populates="fitness_goals") # Relationship with the User class (many-to-one)

class Workout(Base):
    '''This class represents the workouts table in the database'''
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True) # Unique identifier for each workout
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign key to link the workout to a user
    date = Column(Date, nullable=False,index=True) # Date of the workout
    duration = Column(Float) # Duration of the workout in minutes
    type = Column(String) # Type of the workout
    intensity = Column(String) # Intensity of the workout
    calories_burned = Column(Float) # Calories burned during the workout
    notes = Column(Text) # Any additional notes about the workout
    user = relationship("User", back_populates="workouts") # Relationship with the User class (many-to-one)

class NutritionLog(Base):
    '''This class represents the nutrition_logs table in the database'''
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True) # Unique identifier for each nutrition log
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign key to link the nutrition log to a user
    date = Column(Date, nullable=False,index=True) # Date of the nutrition log
    meal_type = Column(String) # Type of meal (e.g. Breakfast, Lunch, Dinner, Snack)
    calories = Column(Integer) # Calories consumed
    proteins = Column(Float) # Proteins consumed in grams
    carbs = Column(Float)  # Carbohydrates consumed in grams
    fats = Column(Float) # Fats consumed in grams
    notes = Column(Text) # Any additional notes about the nutrition log
    user = relationship("User", back_populates="nutrition_logs") # Relationship with the User class (many-to-one)

class SleepRecord(Base):
    '''This class represents the sleep_records table in the database'''
    __tablename__ = 'sleep_records'
    id = Column(Integer, primary_key=True) # Unique identifier for each sleep record
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign key to link the sleep record to a user
    start_time = Column(DateTime, nullable=False,index=True) # Start time of the sleep
    end_time = Column(DateTime, nullable=False) # End time of the sleep
    quality = Column(String) # Quality of the sleep (e.g. Poor, Fair, Good, Excellent)
    deep_sleep_duration = Column(Float) # Duration of deep sleep in hours
    notes = Column(Text) # Any additional notes about the sleep record
    user = relationship("User", back_populates="sleep_records") # Relationship with the User class (many-to-one)

class MoodLog(Base):
    '''This class represents the mood_logs table in the database'''
    __tablename__ = 'mood_logs'
    id = Column(Integer, primary_key=True) # Unique identifier for each mood log
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign key to link the mood log to a user
    date = Column(Date, nullable=False,index=True) # Date of the mood log
    mood = Column(String) # Mood of the user
    stress_level = Column(Integer)  # Stress level of the user
    notes = Column(Text) # Any additional notes about the mood log
    user = relationship("User", back_populates="mood_logs") # Relationship with the User class (many-to-one)

def create_database():
    '''Create the database and the tables'''
    engine = create_engine('sqlite:///health_fitness_app.db', echo=True) # Create a new SQLite database using the create_engine() function
    Base.metadata.create_all(engine) # Create the tables in the database using the metadata.create_all() method

if __name__ == '__main__':
    create_database() # Call the create_database() function to create the database and the tables
