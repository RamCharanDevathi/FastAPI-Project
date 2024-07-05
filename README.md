# FastAPI-Project


This project implements a RESTful API for a supply chain management system using FastAPI, PostgreSQL, and Swagger UI.

## Setup Instructions

### Prerequisites

- Python 3.x installed
- PostgreSQL installed and running
- Pipenv or virtualenv for managing dependencies (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RamCharanDevathi/FastAPI-Project.git
   cd FastAPI-Project

### Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables (database connection, OAuth2 credentials, etc.) in .env file.

### Apply database migrations:

bash
Copy code
alembic upgrade head
Running the Application
bash
Copy code
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.


### Executing Test cases
Running Tests
bash
Copy code
pytest
This will run all the tests located in the tests/ directory.

### Swagger API Documentaion

API Documentation
API documentation can be accessed at http://127.0.0.1:8000/docs.


### Pushing the changes back to git repository
Copy code
Push Your Code

Once you have everything set up locally, add, commit, and push your code to GitHub:

bash
Copy code
git add .
git commit -m "Initial commit: Setup FastAPI project for supply chain management system"
git push origin main
