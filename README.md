# Byron Labs Backend

This is a simple Cybersecurity Incident Reporting API, code test for [Byron Labs](https://github.com/ByronLabs).

The task is to create a simple API that allows users to report cybersecurity incidents. The API should be able to handle CRUD operations for incidents and users. The API should also have features like pagination, filtering, sorting, searching, and authentication.

## Installation

1. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Set the environment variables in a `.env` file at the root of the project

```bash
export JWT_ALGORITHM=your_algorithm # default is HS256
export JWT_SECRET=your_secret_key
export JWT_EXPIRATION=your_expiration_time # default set to 30 minutes (e.g. 30)
```

4. Run the application

```bash
uvicorn app.main:app --reload
```

## Usage

You can use the following endpoints to interact with the API:

- GET /incident/all: Get a list of all incidents
- POST /incident: Create a new incident
- GET /incident/{id}: Get details of a specific incident
- PUT /incident/{id}: Update an incident
- DELETE /incident/{id}: Delete an incident
- POST /login: Login to the API
- POST /logout: Logout from the API
- POST /register: Register a new user

The API should be able to handle the following fields:

- Title
- Description
- Severity (Low, Medium, High)
- Created At
- Updated At
- Reporter Details (Name, Email, Phone Number, Company, etc.)

The API should also have the following features:

- Pagination
- Filtering
- Sorting
- Searching
- Authentication
- Error handling