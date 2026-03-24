from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date

class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    email = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    gender = Column(String)
    current_grade = Column(Integer)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent")

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)
    day_of_week = Column(String)
    time_slot = Column(String)
    teacher_name = Column(String)
    max_students = Column(Integer)

class ClassRegistration(Base):
    __tablename__ = "class_registrations"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    package_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    total_sessions = Column(Integer)
    used_sessions = Column(Integer, default=0)