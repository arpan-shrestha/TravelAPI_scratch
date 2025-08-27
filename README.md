# Travel API

A simple Django-based REST-like API for managing Domestic and International Trips, Services and Blogs. It supports basic CRUD operations (Create, Read, Update, Delete) with JSON responses.

In addition, this project implements a secure token-based authentication system in Django using access tokens and refresh tokens. It allows users to log in, access protected endpoints, and refresh access tokens when they expire (Tokens are stored in a PostgreSQL database).

---

## Features
- List all domestic and international trips
- Add a new trips / service / blog
- Update existing trips / service / blog
- Delete trips / service / blog
- JSON-based responses
- CSRF-exempt for API testing (using Postman / cURL)

---

## Security Features
- User authentication with username and password (hashed in the database).
- Access tokens valid for 1 hour.
- Refresh tokens valid for 15 days.
- Automatic refresh of access tokens using refresh tokens for 15 days.
- Tokens are stored in a PostgreSQL database:
  - access_token, refresh_token
  - Expiry timestamps
  - is_active flag to manage token revocation
- Protected endpoints using @token_required decorator.

---

## Tech Stack
- Python 3
- Django
- PostgreSQL

---

## API Endpoints

### Domestic Trips
- `GET /domestic-destinations/` - List all domestic trips
- `POST /domestic-destinations/add/` - Add a new trip
- `PUT/PATCH /domestic-destinations/<id>/update/` - Update trip
- `DELETE /domestic-destinations/<id>/` - Delete trip

### International Trips
- `GET /international-destinations/` - List all international trips
- `POST /international-destinations/add/` - Add a new trip
- `PUT/PATCH /international-destinations/<id>/update/` -  Update trip
- `DELETE /international-destinations/<id>/` - Delete trip
  
### Services
- `GET /service/` - List all services
- `POST /service/add_service/` - Add a new service
- `PUT/PATCH /service/<id>/update/` - Update service
- `DELETE /service/<id>/delete/` - Delete service
  
### Blogs
- `GET /blog/` - List all blogs
- `POST /blog/add_blog/` - Add a new blog
- `PUT/PATCH /blog/<id>/update/` - Update blog
- `DELETE /blog/<id>/delete/` - Delete blog
---

## Auth Endpoints
1. Login
`POST /auth/login/`

Request body (JSON):
```json
{
  "username": "your_username",
  "password": "your_password",
}
```

Response:
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "access_token_expire": "ISO8601 timestamp",
  "refresh_token_expire": "ISO8601 timestamp"
}
```
- Use the access_token in the ***Authorixation*** header for protected endpoints:
  `Authorization: Bearer <access_token>`

2. Refresh Access Token
`POST /auth/refresh-token/`
Request body (JSON):
```json
{
  "refresh_token": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "access_token_expire": "ISO8601 timestamp",
  "refresh_token_expire": "ISO8601 timestamp"
}
```
- The refresh token generates a new access token when previous one expires.
- Access tokens are overwritten in the database.
---

## Testing with Postman
1. Open **Postman**
2. Add Authorization header for protected endpoints:
   `Authorization: Bearer <access_token>`
3. Choose the method (**GET/POST/PUT/PATCH/DELETE**)
4. Use the endpoint (e.g., `http://127.0.0.1:8000/domestic-destinations/1/update/`)
5. Provide JSON body for POST/PUT/PATCH, e.g.:

```json
{
  "title": "Updated New Trip",
  "description": "An adventurous trip",
  "details_url": "https://example.com/trip"
}
```
