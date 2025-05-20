from datetime import datetime, date
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, DECIMAL,
    Boolean, DateTime, Text, Table
)
from sqlalchemy.orm import relationship
from database import Base

# ---------- ENUMS ----------
class DocumentTypeEnum(str, PyEnum):
    passport = "passport"
    employment_record = "employment_record"
    contract = "contract"
    other = "other"

class VacationTypeEnum(str, PyEnum):
    regular = "regular"
    sick = "sick"
    unpaid = "unpaid"

class VacationStatusEnum(str, PyEnum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"

class RoleTypeEnum(str, PyEnum):
    sector = "sector"
    medical = "medical"

class RoleStatusEnum(str, PyEnum):
    planned = "planned"
    approved = "approved"

# ---------- Association Table ----------
employee_roles = Table(
    "employee_roles",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)

# ---------- EMPLOYEES ----------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employee_code = Column(String(60), unique=True, nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    position = Column(String(100))
    hire_date = Column(Date)
    salary = Column(DECIMAL(10, 2))
    status = Column(Enum("active", "inactive", name="employee_status"), default="active")
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship(
        "Department",
        back_populates="employees",
        foreign_keys=[department_id]
    )

    managed_department = relationship(
        "Department",
        back_populates="manager",
        uselist=False,
        foreign_keys="Department.manager_id"  # строка — для ленивой загрузки
    )

    documents = relationship("Document", back_populates="employee")
    vacations = relationship("Vacation", back_populates="employee")
    users = relationship("User", back_populates="employee")
    roles = relationship("Role", secondary=employee_roles, back_populates="employees")

# ---------- DEPARTMENTS ----------
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    manager_id = Column(Integer, ForeignKey("employees.id"))

    employees = relationship(
        "Employee",
        back_populates="department",
        foreign_keys="Employee.department_id"
    )

    manager = relationship(
        "Employee",
        back_populates="managed_department",
        foreign_keys=[manager_id]
    )

# ---------- USERS ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_active = Column(Boolean, default=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="users")

# ---------- DOCUMENTS ----------
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    document_type = Column(Enum(DocumentTypeEnum), nullable=False)
    file_path = Column(String(255), nullable=False)
    expiration_date = Column(Date)
    upload_date = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="documents")

# ---------- VACATIONS ----------
class Vacation(Base):
    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    vacation_type = Column(Enum(VacationTypeEnum), nullable=False)
    status = Column(Enum(VacationStatusEnum), nullable=False)
    notes = Column(Text)

    employee = relationship("Employee", back_populates="vacations")

# ---------- ROLES ----------
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_type = Column(Enum(RoleTypeEnum), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(RoleStatusEnum), nullable=False)

    employees = relationship("Employee", secondary=employee_roles, back_populates="roles")
