# 📚 Library API

A RESTful API built with FastAPI for managing users, books, and loans in a library system.  
Includes JWT authentication and role-based access control (admin/user).

---

## 🚀 Features

- User registration and login with JWT
- Book creation (admin-only) and listing
- Book loan and return system
- Role-based permissions
- SQLite as database

---

## 🛠️ Setup Instructions (Windows/Linux/Mac)

### 1. 🐍 Install Python

Make sure you have **Python 3.8+** installed.

- [Download Python](https://www.python.org/downloads/)

You can check with:

```bash
python --version
```
# or
```bash
python3 --version
```

### 2. 💻 Install VS Code (recommended)

Download and install VS Code from:

- [Vscode]( https://code.visualstudio.com/)

Also install the Python extension from Microsoft inside VS Code.

### 3. 🧪 Create and activate virtual environment

# Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
# Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### 5. 🧱 Run the application
```bash
uvicorn app.main:app --reload
```

The server will start at:
[Here](http://127.0.0.1:8000)

Swagger documentation is available at:
- [Swagger documentation](http://127.0.0.1:8000/docs)

Redoc documentation is available at:
- [Redoc documentation](http://127.0.0.1:8000/redoc)

### 🗄️ Database initialization
On first run, FastAPI will create the database (library.db) and all tables via SQLAlchemy.
Make sure Base.metadata.create_all() is called in main.py.


### 🗃️ Project Structure
```text
📁library-api/
│
├── .env                     # Environment variables (e.g., DB URL, secrets)
├── .gitignore               # Files and folders to be ignored by Git
├── requirements.txt         # List of Python packages required to run the project
├── README.md                # Project documentation
│
├── 📁app/                     # Main application code
│
│   ├── main.py              # Entry point of the FastAPI application
│   ├── database.py          # SQLAlchemy database connection and session
│   ├── oauth2.py            # JWT authentication and security utilities
│   ├── seed_data.py         # Script to insert initial data (roles, users, books)
│   ├── settings.py          # App configuration and environment loading
│   ├── utils.py             # Helper functions (e.g., password hashing, token logic)
│
│   ├── 📁schemas/             # Pydantic models for request/response validation
│   │   ├── book.py
│   │   ├── loan.py
│   │   ├── role.py
│   │   ├── token.py
│   │   └── user.py
│
│   ├── 📁services/            # Business logic for each domain
│   │   ├── book_service.py
│   │   ├── loan_service.py
│   │   └── user_service.py
│
│   ├── 📁models/              # SQLAlchemy ORM models (database tables)
│   │   ├── book.py
│   │   ├── erole.py         # Enum for user roles (if used)
│   │   ├── loans.py
│   │   ├── roles.py
│   │   ├── user_roles.py    # Join table if roles are many-to-many
│   │   └── users.py
│
│   ├── 📁routers/             # FastAPI route definitions
│   │   ├── book.py
│   │   ├── loan.py
│   │   └── user.py

```

### 🔐 Environment Variables
Create a .env file in the root folder:
```bash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Docker (Optional)
### ✅ Prerequisites

Before building and running the container, make sure you have the following:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with support for Linux containers)
- Internet connection (to download the base image and dependencies)
- Docker Hub open and signed in (optional, only if you want to push the image)

---

### 🐳 Build the Docker Image

1. Open your terminal or CMD and navigate to the root folder of the project where the `Dockerfile` is located.

2. Run the following command to build the Docker image:

```bash
docker build -t library-api .
```

#### This command will:

- Use python:3.13.3 as the base image.

- Copy the requirements.txt and install all dependencies.

- Copy the rest of the project files.

- Launch the app with uvicorn on port 8000.


### ▶️ Run the Docker Container

Once the image is built, you can run the container using:

```bash
docker run -d -p 8000:8000 library-api
```

####This command:

- Runs the container in detached mode (-d).

- Maps port 8000 from the container to port 8000 on your machine.

### 🌐 Access the API

Open your browser and visit:

- [Project](http://localhost:8000)
- [Swagger documentation](http://localhost:8000/docs)
- [Redoc documentation](http://localhost:8000/redoc)


## 📫 Postman Collections
To manually test the API, you can use Postman.

### 🧰 Step-by-step:
Install Postman
- [Download Postman](https://www.postman.com/downloads/)

Import the following files into Postman:
- Library API.postman_collection.json

- Library API.postman_environment.json

In Postman, select the environment "Library API" from the top-right dropdown.

### ⚠️ If using Docker

By default, the Postman environment is set to use:

```bash
http://127.0.0.1:8000
```

If you're running the project using Docker, you must change the environment variable URL to:

```bash
http://localhost:8000
```

### To update this in Postman:

1. Open the "Library API" environment.

2. Locate the URL variable.

3. Replace http://127.0.0.1:8000 with http://localhost:8000.

4. Save the environment and run your requests again.
