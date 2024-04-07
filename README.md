# My API

This is a RESTful API built with FastAPI.

## Structure

The API is structured as follows:

- `app/`: Main application directory
  - `routes/`: Contains all the route files
  - `db/`: Contains the database models

## Setup

1. Clone the repository: `git clone https://github.com/yourusername/yourrepository.git`
2. Navigate to the project directory: `cd yourrepository`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`

## Usage

The API has the following endpoints:

- `GET /students`: Get all students
- `GET /students/{id}`: Get a student by ID
- `POST /students`: Create a new student
- `PUT /students/{id}`: Update a student by ID
- `DELETE /students/{id}`: Delete a student by ID

Each student object has the following structure:

```json
{
  "name": "string",
  "age": 0,
  "address": {
    "city": "string",
    "country": "string"
  }
}