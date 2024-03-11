from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    weight = Column(Float)
    height = Column(Float)
    email = Column(String, unique=True, nullable=False,index=True)
    bio = Column(Text)
    fitness_goals = relationship("FitnessGoal", back_populates="user", cascade="all, delete, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete, delete-orphan")
    nutrition_logs = relationship("NutritionLog", back_populates="user", cascade="all, delete, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete, delete-orphan")
    mood_logs = relationship("MoodLog", back_populates="user", cascade="all, delete, delete-orphan")

class FitnessGoal(Base):
    __tablename__ = 'fitness_goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal = Column(String, nullable=False)
    description = Column(Text)
    target_date = Column(Date)
    completed = Column(Boolean, default=False)
    user = relationship("User", back_populates="fitness_goals")

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False,index=True)
    duration = Column(Float)  # in minutes
    type = Column(String)
    intensity = Column(String)
    calories_burned = Column(Float)
    notes = Column(Text)
    user = relationship("User", back_populates="workouts")

class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False,index=True)
    meal_type = Column(String)
    calories = Column(Integer)
    proteins = Column(Float)  # grams
    carbs = Column(Float)  # grams
    fats = Column(Float)  # grams
    notes = Column(Text)
    user = relationship("User", back_populates="nutrition_logs")

class SleepRecord(Base):
    __tablename__ = 'sleep_records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime, nullable=False,index=True)
    end_time = Column(DateTime, nullable=False)
    quality = Column(String)
    deep_sleep_duration = Column(Float)  # in hours
    notes = Column(Text)
    user = relationship("User", back_populates="sleep_records")

class MoodLog(Base):
    __tablename__ = 'mood_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False,index=True)
    mood = Column(String)
    stress_level = Column(Integer)  # scale 1-10
    notes = Column(Text)
    user = relationship("User", back_populates="mood_logs")

def create_database():
    engine = create_engine('sqlite:///health_fitness_app.db', echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_database()
