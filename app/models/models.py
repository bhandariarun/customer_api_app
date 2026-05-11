"""
models.py — SQLAlchemy ORM Models
Maps Python classes to the existing database tables.
These are used by crud.py to build type-safe queries without raw SQL.
"""

from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Text, ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customerNumber           = Column(Integer, primary_key=True, index=True)
    customerName             = Column(String(50), nullable=False)
    contactLastName          = Column(String(50), nullable=False)
    contactFirstName         = Column(String(50), nullable=False)
    phone                    = Column(String(50), nullable=False)
    addressLine1             = Column(String(50), nullable=False)
    addressLine2             = Column(String(50), nullable=True)
    city                     = Column(String(50), nullable=False)
    state                    = Column(String(50), nullable=True)
    postalCode               = Column(String(15), nullable=True)
    country                  = Column(String(50), nullable=False)
    salesRepEmployeeNumber   = Column(Integer, ForeignKey("employees.employeeNumber"), nullable=True)
    creditLimit              = Column(Numeric(10, 2), nullable=True)

    # Relationships — lazy="selectin" loads them automatically with the parent
    orders   = relationship("Order",   back_populates="customer", lazy="selectin")
    payments = relationship("Payment", back_populates="customer", lazy="selectin")


class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber    = Column(String(50), primary_key=True)
    paymentDate    = Column(Date, nullable=False)
    amount         = Column(Numeric(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="payments")


class Order(Base):
    __tablename__ = "orders"

    orderNumber    = Column(Integer, primary_key=True, index=True)
    orderDate      = Column(Date, nullable=False)
    requiredDate   = Column(Date, nullable=False)
    shippedDate    = Column(Date, nullable=True)
    status         = Column(String(15), nullable=False)
    comments       = Column(Text, nullable=True)
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
