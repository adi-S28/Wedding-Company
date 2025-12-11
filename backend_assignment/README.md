Organization Management Service

A Backend Intern Assignment to build a multi-tenant organization management service using FastAPI and MongoDB.

Overview

This service allows for the creation, management, and authentication of organizations in a multi-tenant architecture. 
- Master Database: Stores metadata about organizations and admins.
- Dynamic Collections: Each organization has its own collection (org_<name>) for data isolation.

Tech Stack

- Framework: FastAPI (Python)
- Database: MongoDB (Motor async driver)
- Authentication: JWT (JSON Web Tokens) with BCrypt password hashing
- Validation: Pydantic

Setup Instructions

Prerequisites
- Python 3.8+
- MongoDB installed and running locally on port 27017.

Installation

1. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Configure Environment (Optional):
   - The application uses default settings (mongodb://localhost:27017).
   - You can override these in config.py or via environment variables.

Running the Application

1. Start the server using Uvicorn:
   uvicorn main:app --reload

2. Access the API documentation (Swagger UI) at:
   - http://localhost:8000/docs

Verification

A verification script is provided to test the core flows (Create -> Login -> Get -> Update -> Delete).

1. Ensure the server is running.
2. In a separate terminal, run:
   python verify_api.py
Design Notes

Architecture & Scalability
- Multi-tenancy: based on collection-based isolation. This scheme offers an acceptable ratio of rational segregation-handling expense with database-level segregation.
- Master Database: A master database which stores and keeps connection strings and metadata. This enables the use of horizontal scaling whereby various organizations may be hosted on varying MongoDB cluster (sharding).
- Async I/O: With the help of Motor, aside of blocking I/O, Fastapi can be used maliciously where concurrency is at a vital level.

Trade-offs
1. Collection Management: The creation of a collection will cause namespace pressure in MongoDB when being created with thousands of organizations. A Discriminator Field pattern (storing all in a single collection using an org id) is better at large scalability with a large number of small tenants but comes at a lower degree of isolation.
2. Dynamic Rename: renaming Collections and synchronization of the data (renameCollection) is rather expensive, and is only atomic within the same database. This would involve hand over migration (Find -> Insert -> Delete) in a sharded set-up.
3. Consistency: Reference to the (Master DB) and Dynamic collection: this does not constitute a single ACID operation (except using MongoDB Multi-Document Transactions), which means that it may fail partially.

Improvements
- Use UUIDs: The existing version is based on MongoDB Object Id. UUIDs are higher quality to external APIs.
- Schema Validation: Impose schemas on the dynamic collections in MongoDB JSON Schema validation.
- Transactions: MongoDB transactions can be used to provide atomicity during the creation of Org + Admin.
