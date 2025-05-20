from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

# ---------- ENUMS ----------
class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class DocumentType(str, Enum):
    passport = "passport"
    employment_record = "employment_record"
    contract = "contract"
    other = "other"

class VacationType(str, Enum):
    regular = "regular"
    sick = "sick"
    unpaid = "unpaid"

class VacationStatus(str, Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"

class RoleType(str, Enum):
    sector = "sector"
    medical = "medical"

class RoleStatus(str, Enum):
    planned = "planned"
    approved = "approved"

# ---------- EMPLOYEE ----------
class EmployeeBase(BaseModel):
    employee_code: str
    last_name: str
    first_name: str
    position: str
    hire_date: date
    salary: Optional[float] = None
    status: EmployeeStatus = EmployeeStatus.active
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None
    status: Optional[EmployeeStatus] = None
    department_id: Optional[int] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# ---------- USER ----------
class UserBase(BaseModel):
    username: str
    email: str
    password: str
    employee_id: Optional[int] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    employee_id: Optional[int] = None

class User(UserBase):
    id: int
    is_active: bool
    registration_date: datetime

    class Config:
        from_attributes = True

# ---------- DEPARTMENT ----------
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str]
    manager_id: Optional[int]

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True

# ---------- DOCUMENT ----------
class DocumentBase(BaseModel):
    employee_id: int
    document_type: DocumentType
    file_path: str
    expiration_date: Optional[date]

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    upload_date: datetime

    class Config:
        from_attributes = True

# ---------- VACATION ----------
class VacationBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    vacation_type: VacationType
    status: VacationStatus
    notes: Optional[str]

class VacationCreate(VacationBase):
    pass

class Vacation(VacationBase):
    id: int

    class Config:
        from_attributes = True

# ---------- ROLE ----------
class RoleBase(BaseModel):
    role_type: RoleType
    start_date: date
    end_date: Optional[date]
    status: RoleStatus

class RoleCreate(RoleBase):
    employee_ids: List[int]  # для связи many-to-many

class Role(RoleBase):
    id: int
    employees: List[Employee] = []

    class Config:
        from_attributes = True
