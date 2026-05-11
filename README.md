# Customer API App

A layered REST API for the ClassicModels database, built with FastAPI and PostgreSQL. Browse, create, update, and delete customer records with related orders and payments automatically included.

## Features

- **RESTful API** – Fully documented with Swagger UI at `/docs`
- **Layered Architecture** – Router, CRUD, Models, and Database layers
- **Structured Logging** – All operations logged at INFO/ERROR levels
- **Health Checks** – Database connectivity verified on startup
- **Pagination** – Query customers with skip/limit parameters
- **Dashboard Counts** – Aggregate counts across all tables
- **Docker Support** – Ready to deploy with Docker Compose

---

## Project Structure

```
customer_api_app/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project metadata
├── .env                       # Environment variables (local development)
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-service orchestration
├── LICENSE                    # MIT License
├── README.md                  # This file
│
└── app/
    ├── crud/
    │   └── crud.py            # Database query & mutation functions
    ├── db/
    │   └── database.py        # SQLAlchemy engine & session factory
    ├── logger/
    │   └── logger.py          # Structured logging setup
    ├── models/
    │   └── models.py          # SQLAlchemy ORM models
    ├── router/
    │   └── router.py          # HTTP endpoint handlers
    ├── schemas/
    │   └── schemas.py         # Pydantic request/response schemas
    └── sql/
        ├── docker-compose.yml # Standalone DB container config
        └── seed.sql           # Initial database schema & data
```

### Layer Responsibilities

1. **Router** (`router.py`) – HTTP request handling, validation, error responses
2. **CRUD** (`crud.py`) – Database queries and mutations (no SQL here)
3. **Models** (`models.py`) – SQLAlchemy ORM table definitions
4. **Database** (`database.py`) – Connection pooling and session management
5. **Schemas** (`schemas.py`) – Request/response data validation

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 16 (or use Docker)

### Local Development

#### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure environment variables

Ensure `.env` exists in the project root:


#### 4. Start PostgreSQL

**Option A: Using Docker (recommended)**


**Option B: Using system PostgreSQL**


#### 5. Run the development server

```bash
uvicorn main:app --port 2000 --reload
```

The API is now available at:
- **API Docs**: http://127.0.0.1:9000/docs
- **Health Check**: http://127.0.0.1:9000/

---

## Docker Deployment

### Full Stack (App + Database)

#### 1. Build and start all services

```bash
docker compose up -d --build
```

This will:
- Build the web service image
- Start PostgreSQL with the seed data
- Start the FastAPI app on port 9000

#### 2. Verify services are running

```bash
docker compose ps
```

```
lists the status of containers belonging to a specific Docker Compose project.
```

#### 3. Access the API

- **API Docs**: http://localhost:9000/docs
- **Health Check**: http://localhost:9000/

#### 4. View logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f db
```

#### 5. Stop and clean up

```bash
# Stop services
docker compose down

# Stop and remove data volumes
docker compose down -v

# Full cleanup (remove images & volumes)
docker compose down -v --rmi all
```

---

## API Endpoints

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers/` | List all customers (paginated) |
| GET | `/customers/{customerNumber}` | Get a specific customer |
| POST | `/customers/` | Create a new customer |
| PATCH | `/customers/{customerNumber}` | Update a customer |
| DELETE | `/customers/{customerNumber}` | Delete a customer |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers/count` | Count of all customers |
| GET | `/orders/count` | Count of all orders |
| GET | `/products/count` | Count of all products |
| GET | `/employees/count` | Count of all employees |
| GET | `/offices/count` | Count of all offices |
| GET | `/payments/count` | Count of all payments |
| GET | `/orderdetails/count` | Count of all order details |
| GET | `/productlines/count` | Count of all product lines |
| GET | `/overall_counts` | All counts (concurrent requests) |

### Example Requests

```bash
# List customers (skip 0, limit 10)
curl http://localhost:2000/customers?skip=0&limit=10

# Get a specific customer
curl http://localhost:2000/customers/103

# Create a new customer
curl -X POST http://localhost:2000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "customerName": "Acme Corp",
    "contactLastName": "Smith",
    "contactFirstName": "John",
    "phone": "555-0123",
    "country": "USA"
  }'

# Get overall counts
curl http://localhost:2000/overall_counts
```

---


## Troubleshooting

### Issue: "Connection refused" on localhost:5436

**Solution**: Ensure PostgreSQL is running and accessible:

```bash
# Check if Postgres container is running
docker ps | grep postgres


### Issue: "Database does not exist" errors

**Solution**: Ensure the seed data was loaded:

```bash
# In Docker
docker compose logs db


### Issue: Web app crashes on Docker Compose startup

**Solution**: Check web service logs:

```bash
docker compose logs web --tail 50
```

---

## License

MIT License – See [LICENSE](LICENSE) file for details.

## Contact

Fusemachine Fellowship