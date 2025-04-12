# Vue Project

A book management system with Vue.js frontend and Flask backend.

## Features

- Manage books, authors, and publishers
- RESTful API for CRUD operations
- Vue.js frontend with component-based architecture
- MySQL database with SQLAlchemy ORM

## Setup

### Prerequisites

- Node.js and npm
- Python 3.x
- MySQL

### Backend Setup

```bash
# Install dependencies
pip install flask flask-cors sqlalchemy pymysql python-dotenv

# Set environment variables in .env file
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password

# Run the backend
Make sure your MySQL database is running.
Use a MySQL client such as MySQL Workbench to connect, and enter your database username and password.
Simply accessing the database through the Python script is not enough—you need to ensure that the connection works and that you have the correct credentials by testing it in a MySQL client first.
python Backend.py
```

### Frontend Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```
