# Backend Inter task API

This is a RESTful API built with FastAPI.

## Structure

The API is structured as follows:

- `app/`: Main application directory
  - `routes/`: Contains all the route files
  - `db/`: Contains the database models

## Setup

1. Clone the repository: `git clone https://github.com/ujjwaltiwariii/Backend_intern_task.git`
2. Navigate to the project directory: `cd Backend_intern_task`
3. Install the dependencies: `pip install -r requirements.txt`
4. Create `.env` file and add `uri= your mongo db uri`
5. Run the server: `uvicorn main:app --reload`

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
```

```json
studentIN{
  "name": "string",
  "age": 0,
  "address": {
    "city": "string",
    "country": "string"
  }

}
