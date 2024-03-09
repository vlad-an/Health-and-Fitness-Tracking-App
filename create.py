from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime
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
    fitness_goals = relationship("FitnessGoal", back_populates="user", cascade="all, delete, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete, delete-orphan")
    nutrition_logs = relationship("NutritionLog", back_populates="user", cascade="all, delete, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete, delete-orphan")

class FitnessGoal(Base):
    __tablename__ = 'fitness_goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal = Column(String, nullable=False)
    target_date = Column(Date)
    user = relationship("User", back_populates="fitness_goals")

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    duration = Column(Float)  # in minutes
    type = Column(String)
    intensity = Column(String)
    user = relationship("User", back_populates="workouts")

class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    meal_type = Column(String)
    calories = Column(Integer)  # Total calories consumed in this meal
    user = relationship("User", back_populates="nutrition_logs")

class SleepRecord(Base):
    __tablename__ = 'sleep_records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    quality = Column(String)  # This could be 'Poor', 'Fair', 'Good', or 'Excellent'
    user = relationship("User", back_populates="sleep_records")

def create_database():
    engine = create_engine('sqlite:///health_fitness_app.db', echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_database()