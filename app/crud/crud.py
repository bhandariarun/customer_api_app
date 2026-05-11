"""
crud.py — The Kitchen Layer
Implements all database operations (Create, Read, Update, Delete) using
SQLAlchemy ORM.

Rules:
  ● Only interacts with the database — no external HTTP calls.
  ● Each CRUD operation is a separate, focused function.
  ● All activity is logged at the appropriate level.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import models
from app.schemas import schemas
from app.logger.logger import get_logger

logger = get_logger(__name__)


def get_customer(db: Session, customer_number: int) -> models.Customer | None:
    """Fetch a single customer by primary key. Returns None if not found."""
    logger.info("READ — fetching customer #%s", customer_number)
    customer = db.get(models.Customer, customer_number)
    if customer is None:
        logger.warning("Customer not found: ID %s", customer_number)
    else:
        logger.info("Customer #%s retrieved successfully.", customer_number)
    return customer


def get_customers(db: Session, skip: int = 0, limit: int = 10) -> list[models.Customer]:
    """
    Fetch a paginated list of customers.
    skip  – number of records to bypass (offset)
    limit – maximum number of records to return
    """
    logger.info("READ — listing customers (skip=%s, limit=%s)", skip, limit)
    customers = (
        db.query(models.Customer)
        .offset(skip)
        .limit(limit)
        .all()
    )
    logger.info("Returned %s customer(s).", len(customers))
    return customers


def create_customer(db: Session, customer_in: schemas.CustomerCreate) -> models.Customer:
    """
    Insert a new customer row.
    The customerNumber is determined by the caller (matches DB schema where it
    is not auto-generated). If your DB uses SERIAL/SEQUENCE, remove it from
    CustomerCreate and drop customer_number from this function.
    """
    logger.info("CREATE — inserting new customer: %s", customer_in.customerName)
    db_customer = models.Customer(**customer_in.model_dump())
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
        logger.info("Customer created successfully: #%s", db_customer.customerNumber)
    except Exception as exc:
        db.rollback()
        logger.error("CREATE failed for customer '%s': %s", customer_in.customerName, exc)
        raise
    return db_customer

def update_customer(
    db: Session,
    customer_number: int,
    customer_in: schemas.CustomerUpdate,
) -> models.Customer | None:
    """
    Partially update an existing customer.
    Only fields explicitly provided (non-None) in customer_in are changed.
    Returns None if the customer does not exist.
    """
    logger.info("UPDATE — modifying customer #%s", customer_number)
    db_customer = db.get(models.Customer, customer_number)
    if db_customer is None:
        logger.warning("UPDATE aborted — customer not found: ID %s", customer_number)
        return None

    update_data = customer_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)

    try:
        db.commit()
        db.refresh(db_customer)
        logger.info("Customer #%s updated successfully. Fields changed: %s",
                    customer_number, list(update_data.keys()))
    except Exception as exc:
        db.rollback()
        logger.error("UPDATE failed for customer #%s: %s", customer_number, exc)
        raise
    return db_customer

def delete_customer(db: Session, customer_number: int) -> bool:
    """
    Delete a customer by primary key.
    Returns True if deleted, False if not found.
    """
    logger.info("DELETE — removing customer #%s", customer_number)
    db_customer = db.get(models.Customer, customer_number)
    if db_customer is None:
        logger.warning("DELETE aborted — customer not found: ID %s", customer_number)
        return False

    try:
        db.delete(db_customer)
        db.commit()
        logger.info("Customer #%s deleted successfully.", customer_number)
    except Exception as exc:
        db.rollback()
        logger.error("DELETE failed for customer #%s: %s", customer_number, exc)
        raise
    return True

def count_customers(db: Session) -> int:
    logger.info("CRUD — executing count query for 'customers' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM customers"))
        logger.info("CRUD — executing count query for 'customers' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'customers': %s", exc)
        return 0

def count_orders(db: Session) -> int:
    logger.info("CRUD — executing count query for 'orders' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM orders"))
        logger.info("CRUD — executing count query for 'orders' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'orders': %s", exc)
        return 0

def count_products(db: Session) -> int:
    logger.info("CRUD — executing count query for 'products' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM products"))
        logger.info("CRUD — executing count query for 'products' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'products': %s", exc)
        return 0

def count_employees(db: Session) -> int:
    logger.info("CRUD — executing count query for 'employees' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM employees"))
        logger.info("CRUD — executing count query for 'employees' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'employees': %s", exc)
        return 0

def count_offices(db: Session) -> int:
    logger.info("CRUD — executing count query for 'offices' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM offices"))
        logger.info("CRUD — executing count query for 'offices' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'offices': %s", exc)
        return 0

def count_payments(db: Session) -> int:
    logger.info("CRUD — executing count query for 'payments' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM payments"))
        logger.info("CRUD — executing count query for 'payments' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'payments': %s", exc)
        return 0

def count_orderdetails(db: Session) -> int:
    logger.info("CRUD — executing count query for 'orderdetails' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM orderdetails"))
        logger.info("CRUD — executing count query for 'orderdetails' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'orderdetails': %s", exc)
        return 0

def count_productlines(db: Session) -> int:
    logger.info("CRUD — executing count query for 'productlines' started")
    try:
        result = db.scalar(text("SELECT COUNT(*) FROM productlines"))
        logger.info("CRUD — executing count query for 'productlines' completed successfully")
        return result if result is not None else 0
    except Exception as exc:
        logger.error("CRUD — database error while counting 'productlines': %s", exc)
        return 0
