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
### Step 3: Assignment Scraping (Basic)
- User should see all assignments for EECS16B Course
    - Labs
    - Homeworks
    - Exams
- Displayed in a table format
    - First column should show assignment name
    - Second column should have associated due date
    - Third column should have any links associated with assignment
- Assignments should be listed in order of due date
    - Earliest due date first
### Step 4: Assignment Scraping
- User should see all assignments for courses selected during course selection
    - Labs
    - Homeworks
    - Exams
- Displayed in a table format
    - First column should show course of assignment
    - Second column should show type of assignment
    - Third column should show assignment name
    - Fourth column should show assignment due date
    - Fifth column should show any links associated with assignment
- Assignments should be listed in order of due date
    - Earliest due date first
### Step 5: Assignments In Scope
- User should see only assignments in scope at the current date
    - Assignments in scope if assigned on or before current date
    - Exams in scope if within one week of current date
### Step 6: Marking Assignment Completion
- Assignments endpoint should have two tabs
    - First tab contains pending assignments
        - Assignments in scope that have yet to be completed
        - Current view of assignments endpoint
    - Second tab contains completed assignments
        - Assignments that have been marked as complete by the user
        - Same view as pending assignments tab except in reverse sorted order
- User can mark unfinished assignments as complete
    - Assignment information is moved to completed assignments tab
- User can mark completed assignments as pending
    - Assignment information is moved to pending assignments tab
- User adds another class
    - All other class assignments should not be affected
    - All new class assignments should be added to pending assignments tab
- User removes a class
    - All other class assignmnets should not be affected
    - All assignments pertaining to removed class should be removed from both pending and completed assignments tabs
### Step 7: Update Pending Assignments List
- User can see most recent scraping date
- User can click a button to search for new pending assignments
    - Assignments assigned after the most recent scraping date that are now in scope should show up in pending assignments
    - Completed assignments should remain unchanged
- Changing course list should update pending assignments for all selected courses
- If a course is removed and not immediately added back but is added back later, all assignments assigned from the start of the course to the current date should show up in pending assignments,
regardless of assignment status when course was in user's course list