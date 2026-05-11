"""
schemas.py — The Blueprints Layer
Defines Pydantic models that validate every piece of data coming in or
going out of the API. The database never sees invalid data thanks to this
layer.

Schema hierarchy
────────────────
  CustomerBase       – shared fields
  ├── CustomerCreate – for POST (no ID; DB auto-assigns it)
  ├── CustomerUpdate – for PATCH (every field optional)
  └── CustomerOut    – what the caller receives (ID + related data)

  PaymentOut  – payment summary embedded in CustomerOut
  OrderOut    – order summary embedded in CustomerOut
"""

from __future__ import annotations

import logging
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from app.logger.logger import get_logger

logger = get_logger(__name__)


# ── Shared validators ─────────────────────────────────────────────────────────

def validate_credit_limit(value: Optional[Decimal]) -> Optional[Decimal]:
    """Validate that credit limit is non-negative."""
    if value is not None and value < 0:
        msg = "creditLimit must be a non-negative number."
        logger.warning("Validation error: %s", msg)
        raise ValueError(msg)
    return value


# ── Payment blueprint ─────────────────────────────────────────────────────────

class PaymentOut(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: date
    amount: Decimal

    model_config = {"from_attributes": True}


# ── Order blueprint ───────────────────────────────────────────────────────────

class OrderOut(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

    model_config = {"from_attributes": True}


# ── Customer blueprints ───────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    """
    Shared fields that mirror every column of the customers table.
    Each field carries the correct Python type that matches the DB column.
    """
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    # ── Validators ────────────────────────────────────────────────────────
    @field_validator("customerName", "contactLastName", "contactFirstName",
                     "phone", "addressLine1", "city", "country")
    @classmethod
    def must_not_be_blank(cls, value: str, info) -> str:
        if not value or not value.strip():
            msg = f"Field '{info.field_name}' must not be blank."
            logger.warning("Validation error: %s", msg)
            raise ValueError(msg)
        return value.strip()

    @field_validator("creditLimit")
    @classmethod
    def credit_limit_non_negative(cls, value: Optional[Decimal]) -> Optional[Decimal]:
        return validate_credit_limit(value)

    @model_validator(mode="after")
    def log_successful_validation(self) -> "CustomerBase":
        logger.debug("Customer schema validated successfully for: %s", self.customerName)
        return self


class CustomerCreate(CustomerBase):
    """
    Used when creating a new customer (POST).
    customerNumber is omitted — the database assigns it.
    """
    pass


class CustomerUpdate(BaseModel):
    """
    Used when updating an existing customer (PATCH).
    Every field is Optional so callers can update only what they need.
    """
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    @field_validator("creditLimit")
    @classmethod
    def credit_limit_non_negative(cls, value: Optional[Decimal]) -> Optional[Decimal]:
        return validate_credit_limit(value)


class CustomerOut(CustomerBase):
    """
    What the caller receives (GET responses).
    Includes the auto-assigned ID, related orders, and payments.
    """
    customerNumber: int
    orders: list[OrderOut] = []
    payments: list[PaymentOut] = []

    model_config = {"from_attributes": True}
