# UniPlanner

UniPlanner is a Django web application designed to assist university students in planning their day-to-day activities effortlessly and efficiently. Explore the application at [uniplanner.onrender.com](https://uniplanner.onrender.com).

## Core Functionalities

- **Events**:
  ![Events Page Screenshot](screenshots/Screenshot 2023-10-24 175848.png)
   - Features an events table for users to add and track upcoming events.
   - Includes a filter bar for easy searching of events by name, displaying matching events along with their date and time.

- **Modules**: 
   - Provides a module page for creating and naming modules.
   - Clicking on a module navigates to a detailed page displaying all information related to that specific module.

- **Deadlines**: 
   - Allows for the addition of project, homework, and other deadlines.
   - Displays crucial deadline information including remaining days, urgency ranking, and optional prioritization which highlights high workload deadlines.
   - Features a completion tick box, and automatic removal of past deadlines.

- **Unanswered Questions**: 
   - Includes a table for jotting down unanswered questions to address later with professors.
   - Features an answer indicator and automatic deletion of answered questions after 24 hours.

## File Structure

- **Templates**:
   - `login.html`: Login and registration page.
   - `index.html`: Main page displaying the event table and modules, extends from `layout.html`.
   - `module.html`: Module-specific information page, extends from `layout2.html`.

- **Static Files**:
   - Contains aesthetic elements like PNG images for enhancing the web app's appearance.

- **models.py**:
   - Houses 6 models encompassing users, events, modules, user-module relations, unanswered questions, and deadlines.
   - Some models feature a `serialize()` function for converting QuerySet data into dictionaries for easier access.

- **urls.py**:
   - Defines all paths linking to the functions in `views.py`.

- **views.py**:
   - Contains the backend logic for the entire web application.





