# API Ikigai NGO Countries

This is an API for managing countries for the Ikigai NGO project.

## Endpoints

### Create Country

**POST** `/countries/`

- **Request Body**: `schemas.CountryCreate`
- **Response Model**: `schemas.CountryInDB`
- **Description**: Creates a new country entry in the database.
Example:
```json
{
  "name": "Country Name",
  "flag": "Url Flag"
}
```

### Read Countries

**GET** `/countries/`

- **Response Model**: `List[schemas.CountryInDB]`
- **Description**: Retrieves a list of all countries from the database.

### Read Country by ID

**GET** `/countries/{country_id}`

- **Response Model**: `schemas.CountryInDB`
- **Description**: Retrieves a specific country by its ID.

### Update Country

**PUT** `/countries/{country_id}`

- **Request Body**: `schemas.CountryUpdate`
- **Response Model**: `schemas.CountryInDB`
- **Description**: Updates the details of an existing country.

Example:
```json
{
  "name": "Country Name",
  "flag": "Url Flag"
}
```

### Delete Country

**DELETE** `/countries/{country_id}`

- **Response Model**: `schemas.CountryInDB`
- **Description**: Deletes a specific country by its ID.

## Deployment

### Requirements

Ensure you have the required dependencies listed in `requirements.txt`.

Generate `requirements.txt`:
```bash
pip freeze > requirements.txt
```
## Docker Deployment

### Build Docker Image:

```bash
docker build -t api-ikigai-ngo-countries .
```
### Run Docker Container:

```bash
docker run -p 8000:80 -e IKIGAI_NGO_DATABASE_URL='postgresql://username:password@host.docker.internal:5439/database' api-ikigai-ngo-countries
```