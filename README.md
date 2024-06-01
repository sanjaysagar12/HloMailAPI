# HloMail API

## API Endpoints

### Register a New User

- **Endpoint:** `POST /register`

- **Description:** Registers a new user and sends an OTP to the provided email for verification.

- **Request Body:**

  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password"
  }
  ```

- **Response:**
  ```json
  {
    "valid": true,
    "message": "User registered successfully, please verify OTP sent to email."
  }
  ```
- **Status Codes:**

  200 OK - Successful registration.

  401 Unauthorized - Invalid request data.

### Verify a User

- **Endpoint:** POST /verify

- **Description:** Verifies a user's email using the OTP sent during registration.

- **Request Body:**

  ```json
  {
    "email": "user@example.com",
    "otp": 123456
  }
  ```

- **Response:**

  ```json
  {
    "valid": true,
    "message": "User verified successfully."
  }
  ```

- **Status Codes:**

  200 OK - Successful verification.
  401 Unauthorized - Invalid OTP or email.

### Login a User

- **Endpoint:** POST /login

- **Description:** Logs in a user and returns an authentication token.

- **Request Body:**

  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```

- **Response:**

  ```json
  {
    "valid": true,
    "message": "Login successful.",
    "token": "your-auth-token"
  }
  ```

- **Status Codes:**

  200 OK - Successful login.

  401 Unauthorized - Invalid email or password.

### Forgot Password

- **Endpoint:** POST /forgot-password

- **Description:** Sends a password reset link to the provided email.

- **Request Body:**

  ````json

  {
    "email": "user@example.com"
  }```
  ````

- **Response:**

  ```json
  {
    "message": "Password reset link sent to your email"
  }
  ```

- **Status Codes:**

  200 OK - Password reset link sent successfully.

  401 Unauthorized - Invalid request data.

  404 Not Found - User not found.

### Reset Password

- **Endpoint:** POST /reset-password

- **Description:** Resets the user's password using the token from the reset link.

- **Url:** `/reset-password?token=your-token`

- **Request Body:**

  ```json
  {
    "new_password": "newpassword"
  }
  ```

- **Response:**

  ```json
  {
    "message": "Password reset successfully"
  }
  ```

- **Status Codes:**

  200 OK - Password reset successfully.

  401 Unauthorized - Invalid or expired token.

  401 Unauthorized - Invalid request data.

### Access Profile

- **Endpoint:** POST /profile

- **Description:** Retrieves the user's profile information if the session token is valid.

- **Headers:**

  Content-Type: application/json

  Token: <your-auth-token> (Required for session verification)

- **Response:**

  ```json
  {
  "valid": true,
  "message": "Token is valid.",
  "username": "username",
  "session_data": { ... },
  "user_data": { ... },
  "client_ip": "client-ip-address"
  }
  ```

- **Status Codes:**

  200 OK - Token is valid, and profile information is returned.

  401 Unauthorized - Invalid or missing token.

### Access Dashboard

- **Endpoint:** POST /dashboard

- **Description:** Retrieves the user's API keys and other dashboard-related information.

- **Headers:**

  Content-Type: application/json

  Token: <your-auth-token> (Required for session verification)

- **Response:**

  ```json
   {
   "valid": true,
   "api_keys": [ ... ]
   }
  ```

- **Status Codes:**

  200 OK - Token is valid, and dashboard information is returned.

  401 Unauthorized - Invalid or missing token.

### Add API Key

- **Endpoint:** POST /add-apikey

- **Description:** Generates a new API key for the user.

- **Headers:**

  Content-Type: application/json

  Token: <your-auth-token> (Required for session verification)

- **Request Body:**

  ```json
  {
    "title": "Project Title",
    "desc": "Project Description"
  }
  ```

- **Response:**

  ```json
  {
    "valid": true,
    "api_key": "generated-api-key"
  }
  ```

- **Status Codes:**

- 200 OK - API key generated successfully.
- 401 Unauthorized - Invalid or missing token.

### Edit API Key

- **Endpoint:** POST /add-apikey

- **Description:** Edit Title and Description of the API Key.

- **Headers:**

  Content-Type: application/json

  Token: <your-auth-token> (Required for session verification)

- **Request Body:**

  ```json
  {
    "api_key": "your-api-key",
    "title": "Project Title",
    "desc": "Project Description"
  }
  ```

- **Response:**

  ```json
  {
    "updated": false,
    "error": "no documents updated",
    "valid": true
  }
  ```

- **Status Codes:**

- 200 OK - API key generated successfully.
- 401 Unauthorized - Invalid or missing token.

### Delete API Key

- **Endpoint:** POST /contact-mail

- **Description:** Delete the API key.

- **Request Body:**

  ```json
  {
    "api_key": "your-api-key"
  }
  ```

- **Response:**

  ```json
  {
    "deleted": true,
    "valid": true
  }
  ```

- **Status Codes:**

  200 OK - Email sent successfully.

  401 Unauthorized - Invalid API key.

### Send Contact Mail

- **Endpoint:** POST /contact-mail

- **Description:** Sends an email to the specified recipient using the provided API key.

- **Request Body:**

  ```json
  {
    "api_key": "your-api-key",
    "recipient_email": "recipient@example.com",
    "subject": "Email Subject",
    "body": "Email Body"
  }
  ```

- **Response:**

  ```json
  {
    "valid": true,
    "message": "Email sent successfully."
  }
  ```

- **Status Codes:**

  200 OK - Email sent successfully.

  401 Unauthorized - Invalid API key.

### Send No Reply Mail

- **Endpoint:** POST /noreply-mail

- **Description:** Sends an email to the specified recipient using the provided API key.

- **Request Body:**

  ```json
  {
    "api_key": "your-api-key",
    "sender": "sender name",
    "recipient": "recipient name",
    "recipient_email": "recipient@example.com",
    "subject": "subject",
    "body": "body"
  }
  ```

- **Response:**

```json
{
  "valid": true,
  "message": "Email sent successfully."
}
```

- **Status Codes:**

  200 OK - Email sent successfully.

  401 Unauthorized - Invalid API key.
