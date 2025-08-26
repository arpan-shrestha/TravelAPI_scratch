# Travel API

A simple Django-based REST-like API for managing Domestic and International Trips, Services and Blogs.  
Supports basic CRUD operations (Create, Read, Update, Delete) with JSON responses.  

---

## Features
- List all domestic and international trips
- Add a new trip
- Update existing trips 
- Delete trips
- JSON-based responses
- CSRF-exempt for API testing (using Postman / cURL)

---

## Tech Stack
- Python 3
- Django
- PostgreSQL

---

## Endpoints

### Domestic Trips
- `GET /domestic-destinations/` 
- `POST /domestic-destinations/add/` 
- `PUT /domestic-destinations/<id>/update/` 
- `PATCH /domestic-destinations/<id>/update/` 
- `DELETE /domestic-destinations/<id>/` 

### International Trips
- `GET /international-destinations/`
- `POST /international-destinations/add/`
- `PUT /international-destinations/<id>/update/`
- `PATCH /international-destinations/<id>/update/`
- `DELETE /international-destinations/<id>/`
  
### Services
- `GET /service/`
- `POST /service/add_service/`
- `PUT /service/<id>/update/`
- `PATCH /service/<id>/update/`
- `DELETE /service/<id>/delete/`
  
### Services
- `GET /blog/`
- `POST /blog/add_blog/`
- `PUT /blog/<id>/update/`
- `PATCH /blog/<id>/update/`
- `DELETE /blog/<id>/delete/`
---

## Testing with Postman
1. Open **Postman**
2. Choose the method (**GET/POST/PUT/PATCH/DELETE**)
3. Use the endpoint (e.g., `http://127.0.0.1:8000/domestic-destinations/1/update/`)
4. Set **Headers** → `Content-Type: application/json`
5. Provide JSON body for POST/PUT/PATCH, e.g.:

```json
{
  "title": "Updated New Trip",
  "description": "An adventurous trip",
  "details_url": "https://example.com/trip"
}
