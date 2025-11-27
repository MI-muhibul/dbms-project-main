# News Blog Management System

A full-featured News Blog application built with Python Flask and MySQL. This system allows users to register, read news, and manages a complete content management system for news articles and users.

## Features

-   **User Authentication**: Secure registration and login system using `Flask-Login` and password hashing.
-   **Role-Based Content**: Users can manage their own news articles.
-   **News Management**: Create, Read, Update, and Delete (CRUD) news articles.
-   **User Management**: Admin-like features to view and manage registered users.
-   **AI Image Generation**: Automatically generates cover images for news articles using AI (Pollinations.ai) based on the article title and content.
-   **Database Seeding**: Includes a setup script to create the database schema.
-   **Responsive Design**: Clean and simple user interface.

## Tech Stack

-   **Backend**: Python, Flask
-   **Database**: MySQL (using `mysql-connector-python`)
-   **Frontend**: HTML, CSS (Jinja2 Templates)
-   **Authentication**: Flask-Login, Werkzeug Security

## Prerequisites

-   Python 3.x
-   MySQL Server (e.g., XAMPP, WAMP, or standalone MySQL)
-   Pip (Python package manager)

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Install Dependencies**:
    Install the required Python packages using pip:
    ```bash
    pip install flask mysql-connector-python flask-login werkzeug
    ```

3.  **Database Configuration**:
    -   Open `database_setup.py` and `app.py`.
    -   Update the `db_config` dictionary with your MySQL credentials (host, user, password, port).
    -   Default configuration (XAMPP):
        ```python
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'port': 3306
        }
        ```

4.  **Initialize Database**:
    Run the setup script to create the database, tables, and seed initial data:
    ```bash
    python database_setup.py
    ```
    *This will create the `news_blog_db` database and tables.*

## Database Schema

```mermaid
## erDiagram



## Swimlane Diagram
<img width="1280" height="906" alt="image" src="https://github.com/user-attachments/assets/b12399b3-7f36-41df-ad2a-f638a77e05b0" />

## Usage

1.  **Start the Application**:
    Run the Flask application:
    ```bash
    python app.py
    ```

2.  **Access the App**:
    Open your web browser and go to:
    `http://127.0.0.1:5000`



## Project Structure

-   `app.py`: Main Flask application file containing routes and logic.
-   `database.py`: Database helper class for managing connections and queries.
-   `database_setup.py`: Script to initialize the database schema and seed data.
-   `templates/`: HTML templates for the application.
-   `static/`: Static files (images, CSS, JS).

## API Endpoints

The application also provides JSON API endpoints:
-   `POST /api/auth/register`: Register a new user.
-   `POST /api/auth/login`: Login user.
-   `GET /api/news`: Get all news items.
-   `POST /api/news`: Create a new news item.
-   `GET /api/users`: Get all users.
