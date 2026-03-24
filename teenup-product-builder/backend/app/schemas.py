from pydantic import BaseModel
from datetime import date
from typing import Optional

class ParentCreate(BaseModel):
    name: str
    phone: str
    email: str

class ParentRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str

class StudentCreate(BaseModel):
    name: str
    dob: date
    gender: str
    current_grade: int
    parent_id: int

class StudentRead(BaseModel):
    id: int
    name: str
    dob: date
    gender: str
    current_grade: int
    parent: Optional[ParentRead]

class ClassCreate(BaseModel):
    name: str
    subject: str
    day_of_week: str
    time_slot: str
    teacher_name: str
    max_students: int

class ClassRead(BaseModel):
    id: int
    name: str
    subject: str
    day_of_week: str
    time_slot: str
    teacher_name: str
    max_students: int

class ClassRegistrationCreate(BaseModel):
    student_id: int

class SubscriptionCreate(BaseModel):
    student_id: int
    package_name: str
    start_date: date
    end_date: date
    total_sessions: int

class SubscriptionRead(BaseModel):
    id: int
    student_id: int
    package_name: str
    start_date: date
    end_date: date
    total_sessions: int
    used_sessions: int