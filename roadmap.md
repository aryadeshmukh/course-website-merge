# Road Map
### Step 1: Register / Login Page
- Store login credentials in database.
    - Credentials need to persist even when server is shut down.
    - Store hashed password instead of plaintext password for security measures.
- Register
    - New user must pick a username that is not being currently used.
    - If registration is successful user is redirected to login page.
    - User can go directly to login page if previously created an account.
- Login
    - User enters login credentials.
    - If credentials are valid, user can proceed.
    - User can go to register page if user has not previously created an account.
