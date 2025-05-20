from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- EMPLOYEE ----------
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee_by_code(db: Session, code: str):
    return db.query(models.Employee).filter(models.Employee.employee_code == code).first()

def get_employees(db: Session):
    return db.query(models.Employee).all()

def search_employees_by_last_name(db: Session, last_name: str):
    return db.query(models.Employee).filter(models.Employee.last_name.ilike(f"%{last_name}%")).all()

def update_employee(db: Session, employee_id: int, updated_data: schemas.EmployeeUpdate):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        return None
    update_fields = updated_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if employee:
        db.delete(employee)
        db.commit()
    return employee


# ---------- DEPARTMENT ----------
def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def update_department(db: Session, department_id: int, updated_data: schemas.DepartmentCreate):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        return None
    update_fields = updated_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if department:
        db.delete(department)
        db.commit()
    return department


# ---------- USER ----------
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        employee_id=user.employee_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, updated_data: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    update_fields = updated_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        if field == "password":
            value = pwd_context.hash(value)
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


# ---------- DOCUMENT ----------
def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def update_document(db: Session, document_id: int, updated_data: schemas.DocumentCreate):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return None
    update_fields = updated_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(document, field, value)
    db.commit()
    db.refresh(document)
    return document

def delete_document(db: Session, document_id: int):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if document:
        db.delete(document)
        db.commit()
    return document


# ---------- VACATION ----------
def create_vacation(db: Session, vacation: schemas.VacationCreate):
    db_vacation = models.Vacation(**vacation.dict())
    db.add(db_vacation)
    db.commit()
    db.refresh(db_vacation)
    return db_vacation

def get_vacations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacation).offset(skip).limit(limit).all()

def update_vacation(db: Session, vacation_id: int, updated_data: schemas.VacationCreate):
    vacation = db.query(models.Vacation).filter(models.Vacation.id == vacation_id).first()
    if not vacation:
        return None
    update_fields = updated_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(vacation, field, value)
    db.commit()
    db.refresh(vacation)
    return vacation

def delete_vacation(db: Session, vacation_id: int):
    vacation = db.query(models.Vacation).filter(models.Vacation.id == vacation_id).first()
    if vacation:
        db.delete(vacation)
        db.commit()
    return vacation


# ---------- ROLE ----------
def create_role(db: Session, role: schemas.RoleCreate):
    employee_objs = db.query(models.Employee).filter(models.Employee.id.in_(role.employee_ids)).all()
    db_role = models.Role(
        role_type=role.role_type,
        start_date=role.start_date,
        end_date=role.end_date,
        status=role.status,
        employees=employee_objs,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def update_role(db: Session, role_id: int, updated_data: schemas.RoleCreate):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        return None
    role.role_type = updated_data.role_type
    role.start_date = updated_data.start_date
    role.end_date = updated_data.end_date
    role.status = updated_data.status
    employee_objs = db.query(models.Employee).filter(models.Employee.id.in_(updated_data.employee_ids)).all()
    role.employees = employee_objs
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
    return role
