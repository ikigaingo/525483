# API Ikigai NGO Languages

This is an API for managing languages for the Ikigai NGO project.

## Endpoints

### Create Language

**POST** `/languages/`

- **Request Body**: `schemas.LanguageCreate`
- **Response Model**: `schemas.Language`
- **Description**: Creates a new language entry in the database.

Example:
```json
{
  "language": "Español"
}
```

### Read Language by ID

**GET** `/languages/{language_id}`

- **Response Model**: `schemas.Language`
- **Description**: Retrieves a specific language by its ID.

### Update Language

**PUT** `/languages/{language_id}`

- **Request Body**: `schemas.LanguageCreate`
- **Response Model**: `schemas.Language`
- **Description**: Updates the details of an existing language.

Example:
```json
{
  "language": "Español"
}
```

### Delete Language

**DELETE** `/languages/{language_id}`

- **Response Model**: `schemas.Language`
- **Description**: Deletes a specific language by its ID.


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
docker build -t api-ikigai-ngo-languages .
```
### Run Docker Container:

```bash
docker run -p 8000:80 -e IKIGAI_NGO_DATABASE_URL='postgresql://username:password@host.docker.internal:5439/database' api-ikigai-ngo-languages
```