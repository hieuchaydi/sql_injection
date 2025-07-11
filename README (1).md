
# SQL Injection Demo Project

This project is a simple Flask-based web application with a SQLite database, designed to demonstrate SQL Injection vulnerabilities and secure query practices. It includes a Tkinter GUI client for easy interaction with the server. The project is intended for educational purposes to highlight the importance of secure database handling.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
The project consists of two main components:

- **Server (`app.py`)**: A Flask application that manages a SQLite database with user data and provides RESTful APIs.
- **Client (`client.py`)**: A Tkinter-based GUI to interact with the Flask server.

The application includes both secure and insecure endpoints to illustrate SQL Injection risks and mitigation techniques.

---

## Features
- **Safe Query Endpoint (`/user_safe`)**: Retrieves a username by ID using parameterized queries to prevent SQL Injection.
- **Unsafe Query Endpoint (`/user_unsafe`)**: Retrieves usernames using raw SQL queries, intentionally vulnerable to SQL Injection for demonstration.
- **List All Users Endpoint (`/users`)**: Safely retrieves all users from the database.
- **Logs Endpoint (`/logs`)**: Displays recent query logs (optional and configurable).
- **Interactive GUI**: Allows users to test endpoints with a user-friendly interface.

---

## Prerequisites
- Python 3.6 or higher
- Required Python packages:
  - `flask`
  - `tkinter` (usually included with Python)
  - `requests`
  - `sqlite3` (built-in with Python)

Install dependencies using:

```bash
pip install flask requests
```

---

## Installation
1. Clone the repository or download the files:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

> **Note:** Create a `requirements.txt` file with the following content if not already present:

```
flask
requests
```

3. No additional configuration is required for the SQLite database, as it is initialized automatically on the first run with sample data.

---

## Usage

### Running the Server
1. Navigate to the project directory.
2. Start the Flask server:

```bash
python app.py
```

- The server will run on `http://localhost:5000`.
- The database (`demo.db`) will be created and populated with sample users (e.g., admin and guest).

### Running the Client
1. Open a new terminal window.
2. Launch the GUI client:

```bash
python client.py
```

- Use the interface to interact with the server (see [Endpoints](#endpoints) below).

### Testing
- Enter a User ID (e.g., `1` or `2`) and click the corresponding buttons to test endpoints.
- Use inputs like `1 OR 1=1` with `/user_unsafe` to demonstrate SQL Injection effects.

---

## Endpoints

| Endpoint       | Method | Description                                   | Parameters         | Response Example                          |
| -------------- | ------ | --------------------------------------------- | ------------------ | ---------------------------------------- |
| `/user_safe`   | GET    | Safely retrieves a username by ID              | `id` (positive int) | `{"username": "admin"}` or `{"error": "User not found"}` |
| `/user_unsafe` | GET    | Unsafely retrieves usernames (vulnerable)      | `id` (any string)  | `{"username": ["admin", "guest"]}` or `{"error": "..."}` |
| `/users`       | GET    | Safely retrieves all users                      | None               | `[{"id": 1, "username": "admin"}, ...]` or `{"error": "No users found"}` |
| `/logs`        | GET    | Retrieves recent query logs (optional)         | None               | `[{"id": 1, "query": "...", ...}, ...]` or `{"error": "..."}` |

---

## Security Notes
- **SQL Injection Demonstration:** The `/user_unsafe` endpoint is deliberately vulnerable to SQL Injection to serve as an educational example. **Do not use this in production.**
- **Logging:** Logging is configured to WARNING level by default to suppress informational messages. To enable detailed logs, modify `logging.basicConfig(level=logging.WARNING)` to `logging.basicConfig(level=logging.INFO)` in `app.py`.
- **Secure Practices:** Use `/user_safe` and `/users` as examples of secure parameterized queries.
- **Production Deployment:** Avoid using `debug=True` in production (currently disabled in `app.py`). Consider deploying with a WSGI server like Gunicorn for better performance and security.

---

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of changes.
4. Ensure code follows the existing style and includes tests if applicable.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
