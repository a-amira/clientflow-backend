#Clientflow API Documentation
## Base URL
http://localhost:8001/api/
## Authentication
### Register
**POST** `/api/auth/register/`
Request:
```json
{
    "username":"newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
