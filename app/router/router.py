"""
router.py — The Front Desk Layer
Defines all HTTP endpoints for the Customer API.
Delegates all database work to crud.py — no SQL lives here.

Endpoints
─────────
  GET  /customers/                   → paginated list
  GET  /customers/{customerNumber}   → single customer with orders & payments
  POST /customers/                   → create a new customer
  PATCH /customers/{customerNumber}  → partially update a customer
  DELETE /customers/{customerNumber} → remove a customer
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import asyncio
import time

from app.crud import crud
from app.schemas import schemas
from app.db.database import get_db, SessionLocal
from app.logger.logger import get_logger

logger = get_logger(__name__)

customer_router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@customer_router.get(
    "/",
    response_model=list[schemas.CustomerOut],
    summary="List all customers",
    description=(
        "Returns a paginated list of customers. "
        "Use **skip** (offset) and **limit** to page through results."
    ),
)
def list_customers(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    logger.info("GET /customers/ — skip=%s, limit=%s", skip, limit)
    customers = crud.get_customers(db, skip=skip, limit=limit)
    logger.info("GET /customers/ — returning %s record(s).", len(customers))
    return customers


@customer_router.get(
    "/{customerNumber}",
    response_model=schemas.CustomerOut,
    summary="Get a specific customer",
    description=(
        "Retrieves full details for one customer including their "
        "**orders** and **payments**. Returns 404 if the customer does not exist."
    ),
)
def get_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info("GET /customers/%s — incoming request.", customerNumber)
    customer = crud.get_customer(db, customer_number=customerNumber)
    if customer is None:
        logger.warning("GET /customers/%s — 404 Not Found.", customerNumber)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer #{customerNumber} not found.",
        )
    logger.info("GET /customers/%s — 200 OK.", customerNumber)
    return customer


@customer_router.post(
    "/",
    response_model=schemas.CustomerOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Adds a new customer record to the database.",
)
def create_customer(customer_in: schemas.CustomerCreate, db: Session = Depends(get_db)):
    logger.info("POST /customers/ — creating customer: %s", customer_in.customerName)
    try:
        new_customer = crud.create_customer(db, customer_in=customer_in)
    except Exception as exc:
        logger.error("POST /customers/ — 500 Internal Server Error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create customer. See server logs for details.",
        )
    logger.info("POST /customers/ — 201 Created: customer #%s", new_customer.customerNumber)
    return new_customer


@customer_router.patch(
    "/{customerNumber}",
    response_model=schemas.CustomerOut,
    summary="Partially update a customer",
    description=(
        "Updates only the fields you provide. "
        "Omitted fields are left unchanged."
    ),
)
def update_customer(
    customerNumber: int,
    customer_in: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
):
    logger.info("PATCH /customers/%s — incoming update.", customerNumber)
    updated = crud.update_customer(db, customer_number=customerNumber, customer_in=customer_in)
    if updated is None:
        logger.warning("PATCH /customers/%s — 404 Not Found.", customerNumber)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer #{customerNumber} not found.",
        )
    logger.info("PATCH /customers/%s — 200 OK.", customerNumber)
    return updated


@customer_router.delete(
    "/{customerNumber}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a customer",
    description="Permanently removes a customer record. Returns 404 if not found.",
)
def delete_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info("DELETE /customers/%s — incoming request.", customerNumber)
    deleted = crud.delete_customer(db, customer_number=customerNumber)
    if not deleted:
        logger.warning("DELETE /customers/%s — 404 Not Found.", customerNumber)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer #{customerNumber} not found.",
        )
    logger.info("DELETE /customers/%s — 204 No Content.", customerNumber)


dashboard_router = APIRouter(tags=["Dashboard Counts"])

@dashboard_router.get("/customers/count")
def get_customers_count(db: Session = Depends(get_db)):
    logger.info("GET /customers/count — incoming request.")
    count = crud.count_customers(db)
    logger.info("GET /customers/count — 200 OK.")
    return count

@dashboard_router.get("/orders/count")
def get_orders_count(db: Session = Depends(get_db)):
    logger.info("GET /orders/count — incoming request.")
    count = crud.count_orders(db)
    logger.info("GET /orders/count — 200 OK.")
    return count

@dashboard_router.get("/products/count")
def get_products_count(db: Session = Depends(get_db)):
    logger.info("GET /products/count — incoming request.")
    count = crud.count_products(db)
    logger.info("GET /products/count — 200 OK.")
    return count

@dashboard_router.get("/employees/count")
def get_employees_count(db: Session = Depends(get_db)):
    logger.info("GET /employees/count — incoming request.")
    count = crud.count_employees(db)
    logger.info("GET /employees/count — 200 OK.")
    return count

@dashboard_router.get("/offices/count")
def get_offices_count(db: Session = Depends(get_db)):
    logger.info("GET /offices/count — incoming request.")
    count = crud.count_offices(db)
    logger.info("GET /offices/count — 200 OK.")
    return count

@dashboard_router.get("/payments/count")
def get_payments_count(db: Session = Depends(get_db)):
    logger.info("GET /payments/count — incoming request.")
    count = crud.count_payments(db)
    logger.info("GET /payments/count — 200 OK.")
    return count

@dashboard_router.get("/orderdetails/count")
def get_orderdetails_count(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count — incoming request.")
    count = crud.count_orderdetails(db)
    logger.info("GET /orderdetails/count — 200 OK.")
    return count

@dashboard_router.get("/productlines/count")
def get_productlines_count(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count — incoming request.")
    count = crud.count_productlines(db)
    logger.info("GET /productlines/count — 200 OK.")
    return count

@dashboard_router.get("/overall_counts")
async def get_overall_counts():
    logger.info("GET /overall_counts — incoming request.")
    logger.info("GET /overall_counts — starting concurrent tasks.")
    start_time = time.time()

    def run_count(func):
        with SessionLocal() as db:
            return func(db)

    try:
        results = await asyncio.gather(
            asyncio.to_thread(run_count, crud.count_customers),
            asyncio.to_thread(run_count, crud.count_orders),
            asyncio.to_thread(run_count, crud.count_products),
            asyncio.to_thread(run_count, crud.count_employees),
            asyncio.to_thread(run_count, crud.count_offices),
            asyncio.to_thread(run_count, crud.count_payments),
            asyncio.to_thread(run_count, crud.count_orderdetails),
            asyncio.to_thread(run_count, crud.count_productlines)
        )
        logger.info("GET /overall_counts — asyncio.gather() completed successfully.")
        
        elapsed_time = time.time() - start_time
        logger.info("GET /overall_counts — total response time: %.4f seconds", elapsed_time)
        
        return {
            "customers": results[0],
            "orders": results[1],
            "products": results[2],
            "employees": results[3],
            "offices": results[4],
            "payments": results[5],
            "orderdetails": results[6],
            "productlines": results[7]
        }
    except Exception as exc:
        logger.error("GET /overall_counts — failed with error: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to retrieve overall counts.")

