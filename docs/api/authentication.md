# API Authentication

Authentication methods for the API.

## JWT Authentication\n\nThe API uses JSON Web Tokens (JWT) for authentication.\n\n### Obtaining a Token\n\nSend a POST request to `/auth/login` with valid credentials.\n\n### Using the Token\n\nInclude the token in the Authorization header of your requests:\n\n```\nAuthorization: Bearer YOUR_TOKEN_HERE\n```
