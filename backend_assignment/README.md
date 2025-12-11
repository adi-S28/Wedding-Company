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
- Multi-tenancy: implemented using collection-based isolation. This approach provides a good balance between logical separation and management overhead compared to database-level isolation.
- Master Database: Acts as the central registry, storing connection strings and metadata. This allows for horizontal scaling where different organizations could reside on different MongoDB clusters (sharding).
- Async I/O: The use of Motor with FastAPI ensures non-blocking I/O, suitable for high-concurrency environments.

Trade-offs
1. Collection Management: Creating a collection per organization can lead to namespace pressure on MongoDB if there are thousands of organizations. A "Discriminator Field" pattern (storing all in one collection with an org_id field) scales better for massive numbers of small tenants but offers less isolation.
2. Dynamic Rename: Renaming collections and syncing data (renameCollection) is an expensive operation and atomic only within the same database. In a sharded setup, this would require manual migration (Find -> Insert -> Delete).
3. Consistency: Updating the Master DB and the Dynamic Collection is not a single ACID transaction (unless utilizing MongoDB Multi-Document Transactions), creating a potential for partial failures.

Improvements
- Use UUIDs: The current implementation uses MongoDB ObjectIds. UUIDs are cleaner for external APIs.
- Schema Validation: Enforce schemas on the dynamic collections using MongoDB JSON Schema validation.
- Transactions: Use MongoDB transactions to ensure atomicity when creating Org + Admin.
