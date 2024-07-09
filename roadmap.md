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
### Step 2: Course Selection Page
- User is given options of courses to choose.
    - Drop down search list.
    - User can type for course in text box and course should show up if it exists.
- User can continue to add courses or delete courses from selected.
- User can indicate when finished adding courses to proceed.
    - User must have at least one course selected to proceed.
- User can log out and go back to register page.
    - All selected courses must be saved for user when user logs back in.
- This page shown after successful registration.
