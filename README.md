## Features

- **Swagger API Documentation:** Access API documentation using Swagger UI.
- **User Registration and Email Verification:** Register user email addresses and verify them.
- **User Authentication:** Allow users to log in to the system.
- **User Profile Management:** Manage user personal information.
- **Recipe Management:** Create, list, search, and view recipes.
- **Recipe Categories:** Categorize recipes based on different categories.
- **User Following System:** Allow users to follow and unfollow other users.
- **User Like System:** Enable users to like recipes.
- **My Page:** Display a personalized page for each user.

## Installation

1. Clone the repository:

   ```bash
    git clone https://github.com/Kilotas/CooksCorner.git


Install dependencies:
pip install -r requirements.txt

Apply database migrations:
python manage.py migrate

Run the development server:
python manage.py runserver


## Features

- **Swagger API Documentation:** Access API documentation using Swagger UI. [View Swagger API Documentation](http://localhost:8000/swagger/)
- **Email Registration and Verification:** Register an email for verification. [Register Email for Verification](http://localhost:8000/register/email/)
- **Email Verification:** Verify a registered email. [Verify Registered Email](http://localhost:8000/email-verify/)
- **User Login:** Log in to the system. [Log in to the System](http://localhost:8000/login/)
- **Personal Information Registration:** Register personal information. [Register Personal Information](http://localhost:8000/register/personal-info/)
- **Recipe Management:** Create, list, search, and view recipes. [Create a New Recipe](http://localhost:8000/recipes/), [List All Recipes](http://localhost:8000/main/), [Retrieve, Update, or Delete a Specific Recipe](http://localhost:8000/recipes/<recipe_id>/)
- **Recipe Categorization:** Categorize recipes based on category. [Categorize Recipes Based on Category](http://localhost:8000/recipes/category/<category>/)
- **Recipe Search:** Search for recipes. [Search for Recipes](http://localhost:8000/recipes/search/)
- **User Management:** List all users. [List All Users](http://localhost:8000/users/), [Follow a User](http://localhost:8000/users/<user_id>/follow/), [Unfollow a User](http://localhost:8000/users/<user_id>/unfollow/)
- **Personalized Page:** View your personalized page. [View Your Personalized Page](http://localhost:8000/mypage/), [Update Your Page](http://localhost:8000/my-page/update)
- **Like System:** Like a recipe. [Like a Recipe](http://localhost:8000/recipes/<recipe_id>/like/)






   
