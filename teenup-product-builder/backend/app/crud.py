from datetime import date
from bson import ObjectId
from fastapi import HTTPException
from .database import (
    parents_collection,
    students_collection,
    classes_collection,
    registrations_collection,
    subscriptions_collection
)

def serialize(doc):
    """Chuyển ObjectId thành string để trả về JSON"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ====================== PARENTS ======================
def create_parent(parent_data):
    result = parents_collection.insert_one(parent_data)
    return serialize(parents_collection.find_one({"_id": result.inserted_id}))

def get_parent(parent_id: str):
    doc = parents_collection.find_one({"_id": ObjectId(parent_id)})
    if not doc:
        raise HTTPException(404, "Parent not found")
    return serialize(doc)

# ====================== STUDENTS ======================
def create_student(student_data):
    result = students_collection.insert_one(student_data)
    return serialize(students_collection.find_one({"_id": result.inserted_id}))

def get_student(student_id: str):
    doc = students_collection.find_one({"_id": ObjectId(student_id)})
    if not doc:
        raise HTTPException(404, "Student not found")
    # Lấy thêm thông tin parent
    if "parent_id" in doc:
        parent = parents_collection.find_one({"_id": ObjectId(doc["parent_id"])})
        if parent:
            doc["parent"] = serialize(parent)
    return serialize(doc)

# ====================== CLASSES ======================
def create_class(class_data):
    result = classes_collection.insert_one(class_data)
    return serialize(classes_collection.find_one({"_id": result.inserted_id}))

def get_classes_by_day(day: str = None):
    query = {} if not day else {"day_of_week": day}
    return [serialize(doc) for doc in classes_collection.find(query)]

# ====================== REGISTRATIONS ======================
def register_to_class(class_id: str, student_id: str):
    # Kiểm tra lớp tồn tại
    class_obj = classes_collection.find_one({"_id": ObjectId(class_id)})
    if not class_obj:
        raise HTTPException(404, "Class not found")

    # Kiểm tra sĩ số
    current_students = registrations_collection.count_documents({"class_id": class_id})
    if current_students >= class_obj["max_students"]:
        raise HTTPException(400, "Lớp đã đầy")

    # Kiểm tra trùng lịch (cùng ngày + cùng khung giờ)
    student_regs = list(registrations_collection.find({"student_id": student_id}))
    for reg in student_regs:
        cls = classes_collection.find_one({"_id": ObjectId(reg["class_id"])})
        if cls and cls["day_of_week"] == class_obj["day_of_week"] and cls["time_slot"] == class_obj["time_slot"]:
            raise HTTPException(400, "Trùng lịch học")

    # Kiểm tra gói học
    sub = subscriptions_collection.find_one({"student_id": student_id})
    if not sub or sub["end_date"] < str(date.today()) or sub.get("used_sessions", 0) >= sub["total_sessions"]:
        raise HTTPException(400, "Gói học không hợp lệ hoặc đã hết buổi")

    reg = {
        "class_id": class_id,
        "student_id": student_id
    }
    result = registrations_collection.insert_one(reg)
    return {"id": str(result.inserted_id), "message": "Đăng ký thành công"}

def delete_registration(reg_id: str):
    reg = registrations_collection.find_one({"_id": ObjectId(reg_id)})
    if not reg:
        raise HTTPException(404, "Registration not found")

    # Hoàn 1 buổi (theo logic đề bài)
    sub = subscriptions_collection.find_one({"student_id": reg["student_id"]})
    if sub:
        new_used = max(0, sub.get("used_sessions", 0) - 1)
        subscriptions_collection.update_one(
            {"_id": sub["_id"]},
            {"$set": {"used_sessions": new_used}}
        )

    registrations_collection.delete_one({"_id": ObjectId(reg_id)})
    return {"message": "Đã hủy đăng ký và hoàn 1 buổi"}

# ====================== SUBSCRIPTIONS ======================
def create_subscription(sub_data):
    result = subscriptions_collection.insert_one(sub_data)
    return serialize(subscriptions_collection.find_one({"_id": result.inserted_id}))

def use_session(sub_id: str):
    result = subscriptions_collection.update_one(
        {"_id": ObjectId(sub_id)},
        {"$inc": {"used_sessions": 1}}
    )
    if result.modified_count == 0:
        raise HTTPException(404, "Subscription not found")
    return serialize(subscriptions_collection.find_one({"_id": ObjectId(sub_id)}))

def get_subscription(sub_id: str):
    doc = subscriptions_collection.find_one({"_id": ObjectId(sub_id)})
    if not doc:
        raise HTTPException(404, "Subscription not found")
    return serialize(doc)