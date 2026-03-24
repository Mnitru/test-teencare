from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

# ====================== BASE ======================
class MongoBaseModel(BaseModel):
    id: Optional[str] = Field(None, alias="id")

    class Config:
        populate_by_name = True
        json_schema_extra = {"example": {}}


# ====================== PARENTS ======================
class ParentCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr


class ParentOut(MongoBaseModel):
    name: str
    phone: str
    email: EmailStr


# ====================== STUDENTS ======================
class StudentCreate(BaseModel):
    name: str
    dob: date
    gender: str
    current_grade: int
    parent_id: str


class StudentOut(MongoBaseModel):
    name: str
    dob: date
    gender: str
    current_grade: int
    parent_id: str
    parent: Optional[ParentOut] = None


# ====================== CLASSES ======================
class ClassCreate(BaseModel):
    name: str
    subject: str
    day_of_week: str
    time_slot: str
    teacher_name: str
    max_students: int


class ClassOut(MongoBaseModel):
    name: str
    subject: str
    day_of_week: str
    time_slot: str
    teacher_name: str
    max_students: int


# ====================== REGISTRATIONS ======================
class RegistrationCreate(BaseModel):
    class_id: str
    student_id: str


class RegistrationOut(MongoBaseModel):
    class_id: str
    student_id: str


# ====================== SUBSCRIPTIONS ======================
class SubscriptionCreate(BaseModel):
    student_id: str
    package_name: str
    start_date: date
    end_date: date
    total_sessions: int


class SubscriptionOut(MongoBaseModel):
    student_id: str
    package_name: str
    start_date: date
    end_date: date
    total_sessions: int
    used_sessions: int