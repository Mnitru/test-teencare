# TeenCare Mini LMS – Hướng dẫn chạy project

Tài liệu này hướng dẫn cách chạy lại project backend + frontend từ đầu, bao gồm cả chạy bằng Docker và chạy local.

---

# 1. Yêu cầu môi trường

Cài đặt trước:

* Python 3.10+
* Node.js 18+
* Docker & Docker Compose (khuyến nghị)

Kiểm tra:

```bash
python --version
node --version
docker --version
```

---

# 2. Cấu trúc project (ví dụ)

```
project-root/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml
```

---

# 3. Cách chạy nhanh nhất (Khuyến nghị) – Docker

## Bước 1 – Build và run

Tại thư mục root:

```bash
docker-compose up --build
```

Hoặc chạy background:

```bash
docker-compose up -d --build
```

---

## Bước 2 – Truy cập

Frontend:

```
http://localhost:3000
```

Backend API docs:

```
http://localhost:8000/docs
```

---

## Bước 3 – Stop

```bash
docker-compose down
```

---

# 4. Chạy Backend local (không Docker)

## Bước 1 – Tạo virtual environment

```bash
cd backend

python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

## Bước 2 – Cài dependencies

```bash
pip install -r requirements.txt
```

---

## Bước 3 – Tạo database tables

Quan trọng: đảm bảo có dòng này trong `main.py`:

```python
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
```

---

## Bước 4 – Run server

```bash
uvicorn main:app --reload
```

Server chạy tại:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

# 5. Chạy Frontend local

## Bước 1

```bash
cd frontend
```

## Bước 2

```bash
npm install
```

## Bước 3

Sửa API base URL trong `App.jsx` nếu chạy local:

```javascript
const API = "http://localhost:8000";
```

---

## Bước 4 – Run

```bash
npm start
```

Frontend chạy tại:

```
http://localhost:3000
```

---

# 6. Reset database (khi lỗi)

Nếu dùng SQLite:

```bash
rm database.db
```

Sau đó restart server:

```bash
uvicorn main:app --reload
```

---

# 7. Test nhanh API

## Tạo Parent

POST

```
/api/parents
```

Body:

```json
{
  "name": "Test",
  "phone": "123",
  "email": "test@gmail.com"
}
```

---

## Lấy danh sách Parents

GET

```
/api/parents
```

---

# 8. Lỗi thường gặp

## 500 Internal Server Error

Nguyên nhân phổ biến:

* Chưa create tables
* Database chưa chạy
* Thiếu commit()
* Sai connection string

---

## no such table

Fix:

```python
Base.metadata.create_all(bind=engine)
```

---

## Connection refused

Kiểm tra:

```bash
docker ps
```

---

# 9. Lệnh hữu ích

Restart docker:

```bash
docker-compose down
docker-compose up --build
```

Xem log:

```bash
docker-compose logs -f
```

---

# 10. Database schema (Mô tả sơ lược)

Hệ thống gồm 3 bảng chính:

## parents

| Field | Type    | Description   |
| ----- | ------- | ------------- |
| id    | integer | Primary key   |
| name  | string  | Tên phụ huynh |
| phone | string  | Số điện thoại |
| email | string  | Email         |

---

## students

| Field     | Type    | Description               |
| --------- | ------- | ------------------------- |
| id        | integer | Primary key               |
| name      | string  | Tên học sinh              |
| age       | integer | Tuổi                      |
| parent_id | integer | Foreign key -> parents.id |

Quan hệ:

Parent (1) ---- (N) Student

---

## classes

| Field       | Type    | Description |
| ----------- | ------- | ----------- |
| id          | integer | Primary key |
| name        | string  | Tên lớp     |
| description | string  | Mô tả       |

Quan hệ nhiều‑nhiều (nếu có):

students_classes

| student_id |
| class_id |

---

# 11. Data seed (ví dụ dữ liệu mẫu)

Bạn có thể seed dữ liệu bằng script Python hoặc SQL.

Ví dụ JSON seed:

## Parents (2 records)

```json
[
  {
    "name": "Nguyen Van A",
    "phone": "0900000001",
    "email": "parent1@gmail.com"
  },
  {
    "name": "Tran Thi B",
    "phone": "0900000002",
    "email": "parent2@gmail.com"
  }
]
```

---

## Students (3 records)

```json
[
  {
    "name": "Student 1",
    "age": 10,
    "parent_id": 1
  },
  {
    "name": "Student 2",
    "age": 11,
    "parent_id": 1
  },
  {
    "name": "Student 3",
    "age": 9,
    "parent_id": 2
  }
]
```

---

## Classes (2–3 records)

```json
[
  {
    "name": "Math",
    "description": "Basic math class"
  },
  {
    "name": "English",
    "description": "English communication"
  },
  {
    "name": "Science",
    "description": "Basic science"
  }
]
```

---

# 12. Các endpoint chính

Base URL:

```
http://localhost:8000/api
```

---

## Parent APIs

### Create parent

POST

```
/api/parents
```

Body:

```json
{
  "name": "Test",
  "phone": "123",
  "email": "test@gmail.com"
}
```

---

### Get parent by id

GET

```
/api/parents/1
```

---

### Get all parents

GET

```
/api/parents
```

---

## Student APIs

### Create student

POST

```
/api/students
```

```json
{
  "name": "Student 1",
  "age": 10,
  "parent_id": 1
}
```

---

### Get all students

GET

```
/api/students
```

---

## Class APIs

### Create class

POST

```
/api/classes
```

```json
{
  "name": "Math",
  "description": "Basic math"
}
```

---

### Get all classes

GET

```
/api/classes
```

---

# 13. Script curl demo API

## Create parent

```bash
curl -X POST http://localhost:8000/api/parents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Parent",
    "phone": "0999999999",
    "email": "demo@gmail.com"
  }'
```

---

## Get parents

```bash
curl http://localhost:8000/api/parents
```

---

## Create student

```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Student",
    "age": 10,
    "parent_id": 1
  }'
```

---

# Done


