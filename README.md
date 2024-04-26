# Byron Labs FastAPI Incident Management System

This is a simple Cybersecurity Incident Reporting API, code test for [Byron Labs](https://github.com/ByronLabs).

The task is to create a simple API that allows users to report cybersecurity incidents. The API should be able to handle CRUD operations for incidents and users. The API should also have features like pagination, filtering, sorting, searching, and authentication.

## Overview

This project is a FastAPI-based incident management system. It provides RESTful endpoints for managing incidents, reporters, and authentication, along with various utilities for handling security, pagination, and sorting. The application uses JWT for authentication and supports features like query-based filtering and pagination for efficient data retrieval.

## Installation

To set up and run this FastAPI project locally, follow these steps:

1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables: Create a `.env` file in the project root with the necessary environment variables.

```bash
export JWT_ALGORITHM=your_algorithm # default is HS256
export JWT_SECRET=your_secret_key
export JWT_EXPIRATION=your_expiration_time # default set to 30 minutes (e.g. 30)
```

## Running the application

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --reload
```
This will start the server in development mode with hot-reload enabled. The default URL for accessing the application is `http://localhost:8000`.

### Development Environment

To ensure the correct Node.js version is used, this project includes an `.nvmrc` file. The recommended Node.js version for this project is:

```plaintext
v20.11.1
```

## Endpoints

### Authentication Endpoints

- **POST /auth/login**: Authenticate a user and return a JWT access token.
- **GET /auth/me**: Get information about the currently authenticated user.

### Credentials

To access the FastAPI endpoints, use the following test credentials:

- **Username: `john.doe`**
- **Password: `byronlabs`**

These credentials can be used to authenticate with the /auth/login endpoint to obtain a JWT token for further requests.

### Incident Endpoints

- **GET /incident/all**: Retrieve all incidents with optional pagination and sorting.
- **GET /incident/{id}**: Retrieve a specific incident by its UUID.
- **POST /incident/**: Create a new incident.
- **PUT /incident/{id}**: Update an existing incident by its UUID.
- **DELETE /incident/{id}**: Delete an incident by its UUID.

### Reporter Endpoints

- **GET /reporter/all**: Retrieve all reporters with optional pagination and filtering.