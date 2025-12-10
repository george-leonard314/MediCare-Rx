# MediCare-Rx

MediCare-Rx is a comprehensive pharmacy management system that enables customers to order medications online and allows pharmacy staff to manage orders, inventory, and customer accounts. The system is built with a microservices architecture using Python Flask for both frontend and backend services.

## Overview

MediCare-Rx provides three main interfaces:
- **Customer Portal**: For customers to browse medications, place orders, and track their order history
- **Employee Portal**: For pharmacists and administrators to manage orders, customers, and staff
- **Warehouse CLI**: A command-line interface for warehouse staff to manage medication inventory

## Architecture

The system consists of four main components:

1. **Database Service**: SQLite database initialization and schema management
2. **API Server**: RESTful API built with Flask and Connexion for backend operations
3. **Customer Frontend**: Web interface for customers
4. **Employee Frontend**: Web interface for pharmacy staff

All services are containerized using Docker and orchestrated with Docker Compose.

### Technology Stack

- **Backend**: Python 3.12, Flask, Connexion, SQLAlchemy
- **Frontend**: Flask with Jinja2 templates, HTML/CSS
- **Database**: SQLite
- **Containerization**: Docker, Docker Compose
- **API Documentation**: OpenAPI 3.0 (Swagger)

## Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.12+ (for local development)
- Git

## Installation & Deployment

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/george-leonard314/MediCare-Rx.git
cd MediCare-Rx
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the services:
   - Customer Portal: http://localhost:8081
   - Employee Portal: http://localhost:8089
   - API Server: http://localhost:8083/api

### Manual Installation (Development)

#### Database Setup

```bash
cd Database
pip install -r requirements.txt
python create_db.py
```

#### API Server

```bash
cd Server
pip install -r requirements.txt
python server.py
```

#### Customer Frontend

```bash
cd Frontend_Customer
pip install -r requirements.txt
python frontend_customer.py
```

#### Employee Frontend

```bash
cd Frontend_Employee
pip install -r requirements.txt
python frontend_employee.py
```

#### Warehouse CLI

```bash
cd "Warehouse CLI"
pip install -r requirements.txt
python stock_manager_cli.py
```

## Usage

### Customer Portal

1. Navigate to http://localhost:8081
2. Register a new account or login with existing credentials
3. Browse available medications
4. Place orders by selecting medication, quantity, and providing delivery details
5. View order history and status

**Default Customer Credentials:**
- Username: `lester`
- Password: `1234` (hashed in database)

### Employee Portal

The employee portal has role-based access for pharmacists and administrators.

**Default Employee Credentials:**

Admin/Pharmacist:
- Username: `admin_pharm_518`
- Password: `password`

Pharmacist:
- Username: `pharm_518`
- Password: `password`

Warehouse Staff:
- Username: `warehouse_518`
- Password: `password`

**Features:**
- View and manage customer orders
- Approve or reject medication requests
- Manage customer accounts
- View medication inventory
- Admin: Manage staff accounts

### Warehouse CLI

The CLI tool allows warehouse staff to manage medication inventory.

**Login Credentials:**
- Username: `admin`
- Password: `password`

**Available Commands:**
- `list` - Display all medications in stock
- `add` - Add new medication to inventory
- `update` - Update existing medication details
- `remove` - Remove medication from inventory
- `logout` - Exit the application

## API Documentation

The API server provides OpenAPI/Swagger documentation accessible at:
http://localhost:8083/api/ui

### Key API Endpoints

#### Customer Operations
- `POST /api/customer/register` - Register new customer
- `POST /api/customer/login` - Customer login
- `GET /api/customer/{customer_id}` - Get customer details
- `GET /api/customer/all` - List all customers

#### Order Operations
- `POST /api/customer/order` - Create new order
- `GET /api/order/{order_id}` - Get order details
- `GET /api/order/all` - List all orders
- `PUT /api/order/{order_id}` - Update order status

#### Stock Operations
- `GET /api/stock` - List all medications
- `POST /api/stock` - Add medication
- `PUT /api/stock/{medicine_id}` - Update medication
- `DELETE /api/stock/{medicine_id}` - Remove medication

#### Staff Operations
- `POST /api/staff/login` - Staff login
- `GET /api/staff/{staff_id}` - Get staff details
- `POST /api/staff` - Create staff account
- `PUT /api/staff/{staff_id}` - Update staff details

## Project Structure

```
MediCare-Rx/
├── Database/               # Database initialization and schema
│   ├── create_db.py       # Database creation script with sample data
│   ├── db_config.py       # SQLAlchemy models (Staff, Customer, Order, Stock)
│   └── config.py          # Configuration loader
├── Server/                # REST API backend
│   ├── server.py          # Main API server entry point
│   ├── api.yml            # OpenAPI specification
│   ├── customer_functions.py    # Customer-related endpoints
│   ├── admin_functions.py       # Admin operations
│   ├── pharmacist_functions.py  # Pharmacist operations
│   └── stock_functions.py       # Inventory management
├── Frontend_Customer/     # Customer web interface
│   ├── frontend_customer.py     # Flask application
│   ├── customer_functions.py    # Customer API client
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
├── Frontend_Employee/     # Employee web interface
│   ├── frontend_employee.py     # Flask application
│   ├── admin_functions.py       # Admin operations
│   ├── pharmacist_functions.py  # Pharmacist operations
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
├── Warehouse CLI/         # Command-line inventory tool
│   ├── stock_manager_cli.py     # CLI application
│   ├── stock_functions.py       # Inventory operations
│   └── auth.py                  # CLI authentication
├── compose.yaml           # Docker Compose configuration
├── *.Dockerfile          # Docker build files for each service
└── README.md             # This file
```

## Database Schema

### Tables

**customers**
- customer_id (Primary Key)
- full_name, username, password
- sex, age, height, weight
- email, phone
- validation (account status)

**staff**
- employee_id (Primary Key)
- full_name, username, password
- employee_type (1: Admin/Pharmacist, 2: Pharmacist, 3: Warehouse)
- email, phone

**orders**
- order_id (Primary Key)
- medicine_id, customer_id (FK), employee_id (FK)
- date, medicine_quantity, address, subtotal
- reason_customer, status, reason_employee

**stock**
- medicine_id (Primary Key)
- medicine_name (unique)
- medicine_quantity, price_stuck
- description

## Security Considerations

- All passwords are hashed using SHA-256
- Session-based authentication for web interfaces
- Role-based access control for employee portal
- Input validation on forms and API endpoints

## Development

### Running Tests

Currently, the project uses manual testing. To verify the system:

1. Start all services with Docker Compose
2. Test customer registration and login
3. Test order placement and approval workflow
4. Test inventory management via CLI and web interface

### Configuration

Configuration files are located in each service directory:
- `server.ini` - Database and API server settings
- `customer.ini` - Customer frontend settings
- `employee.ini` - Employee frontend settings
- `warehouse.ini` - Warehouse CLI settings

Default settings use SQLite with a shared database volume mounted in all containers.

## Sample Data

The database initialization script (`Database/create_db.py`) creates sample data:

**Sample Customers:**
- Lester Crest (username: `lester`, password: `1234`)
- Lamar Davis (username: `lamar`, password: `1234`)

**Sample Staff:**
- Michael De Santa - Admin/Pharmacist
- Franklin Clinton - Pharmacist
- Trevor Philips - Warehouse Staff

**Sample Medications:**
- Ibuprofen - For headaches (€2/unit, 100 in stock)
- Paracetamol - General purpose (€3/unit, 200 in stock)

**Sample Orders:**
- Order #0: 5 units of Ibuprofen (approved)
- Order #1: 10 units of Paracetamol (rejected)

## Troubleshooting

### Port Conflicts
If you encounter port conflicts, modify the port mappings in `compose.yaml`.

### Database Issues
To reset the database:
```bash
docker-compose down -v
docker-compose up --build
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for educational purposes.

## Contact

For questions or support, please open an issue on the GitHub repository.
