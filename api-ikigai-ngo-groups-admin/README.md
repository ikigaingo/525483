# API Ikigai NGO Groups Admin API

This is an API built with FastAPI and SQLAlchemy for managing group information. The API allows creating, reading, updating, and deleting groups, as well as associating them with organizations and countries.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Migrations](#migrations)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
```


