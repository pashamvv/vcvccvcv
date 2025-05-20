from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Employees ----------
@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employees/search/", response_model=List[schemas.Employee])
def search_employees(last_name: str, db: Session = Depends(get_db)):
    return crud.search_employees_by_last_name(db, last_name)

@app.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    updated = crud.update_employee(db, employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@app.delete("/employees/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted

# ... (остальные CRUD endpoints для других моделей остаются такими же)


# ---------- Departments ----------

@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)


@app.get("/departments/", response_model=List[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip, limit)


@app.get("/departments/{department_id}", response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@app.put("/departments/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    updated = crud.update_department(db, department_id, department)
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated


@app.delete("/departments/{department_id}", response_model=schemas.Department)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_department(db, department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
    return deleted


# ---------- Users ----------

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted


# ---------- Documents ----------

@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return crud.create_document(db, document)


@app.get("/documents/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documents(db, skip, limit)


@app.put("/documents/{document_id}", response_model=schemas.Document)
def update_document(document_id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    updated = crud.update_document(db, document_id, document)
    if not updated:
        raise HTTPException(status_code=404, detail="Document not found")
    return updated


@app.delete("/documents/{document_id}", response_model=schemas.Document)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_document(db, document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return deleted


# ---------- Vacations ----------

@app.post("/vacations/", response_model=schemas.Vacation)
def create_vacation(vacation: schemas.VacationCreate, db: Session = Depends(get_db)):
    return crud.create_vacation(db, vacation)


@app.get("/vacations/", response_model=List[schemas.Vacation])
def read_vacations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vacations(db, skip, limit)


@app.put("/vacations/{vacation_id}", response_model=schemas.Vacation)
def update_vacation(vacation_id: int, vacation: schemas.VacationCreate, db: Session = Depends(get_db)):
    updated = crud.update_vacation(db, vacation_id, vacation)
    if not updated:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return updated


@app.delete("/vacations/{vacation_id}", response_model=schemas.Vacation)
def delete_vacation(vacation_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_vacation(db, vacation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return deleted


# ---------- Roles ----------

@app.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)


@app.get("/roles/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_roles(db, skip, limit)


@app.put("/roles/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role: schemas.RoleCreate, db: Session = Depends(get_db)):
    updated = crud.update_role(db, role_id, role)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated


@app.delete("/roles/{role_id}", response_model=schemas.Role)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_role(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted
