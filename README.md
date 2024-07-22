# Issue Monitor - Backend

## Overview

The backend of the Issue Monitor web application is developed using Flask and Postgres. It handles user authentication, project management, issue tracking, and user roles. The API endpoints are used by the frontend to interact with the database and perform CRUD operations.

## Features

- **User Authentication:** Allows users to register, log in, and manage their authentication tokens.
- **Project Management:** Endpoints to create, view, update, and delete projects.
- **Issue Tracking:** Endpoints to create, view, update, and delete issues within projects.
- **User Management:** Admins and Project Managers can add or remove users from projects.
- **Role-based Access Control:** Users have roles such as Admin, Project Manager, and Member, with specific permissions.

## Installation

To set up the backend locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/vedprakashsigh/issue-monitor-backend
   cd issue-monitor-backend/
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**

   Update the database configuration in `config.py` with your Postgres details.

5. **Run the Development Server:**

   ```bash
   flask run
   ```

6. **Access the API:**

   The backend will be available at `http://localhost:5000`.

## Endpoints

### **Authentication:**

- `POST /api/auth/register`: Register a new user.
- `POST /api/auth/login`: Authenticate a user and receive a token.

### **Projects:**

- `GET /api/projects`: Get a list of projects (you might want to include filtering or specify which user's projects to list).
- `POST /api/projects`: Create a new project.
- `PATCH /api/projects/<id>`: Update a project.
- `DELETE /api/projects/<id>`: Delete a project.

### **Issues:**

- `GET /api/projects/<project_id>/issues`: Get issues for a specific project.
- `POST /api/projects/<project_id>/issues`: Create a new issue.
- `PATCH /api/issues/<issue_id>`: Update an issue.
- `DELETE /api/issues/<issue_id>`: Delete an issue.

### **Users:**

- `GET /api/users`: Get a list of all users.
- `POST /api/projects/<project_id>/add_user`: Add a user to a project.
- `POST /api/projects/<project_id>/remove_user`: Remove a user from a project.

### **Logs:**

- `GET /api/logs`: Get a list of all logs if not given `count` as query parameter, else gives the last `count` logs.

## Configuration

- **Database Configuration:** Update the `SQLALCHEMY_DATABASE_URI` in `.env` with your database details.
- **JWT Configuration:** Set the `SECRET_KEY` and `JWT_SECRET_KEY` in `.env` for token generation and validation.

## Contributing

If you would like to contribute to the backend, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bugfix.
- Make your changes and test thoroughly.
- Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more detailed documentation on the frontend, please refer to the [Frontend README](https://github.com/vedprakashsigh/issue-monitor-frontend/).
