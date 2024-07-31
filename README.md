# Star Wars Flask Application

Deployed on Render at: https://capstone-starwars.onrender.com

## Overview

This is a Flask-based web application that utilizes data from the SWAPI - the Star Wars API (link at bottom of the page). The application provides various features such as user registration, login, profile management, and commenting on different Star Wars elements including characters, films, starships, vehicles, species, and planets. The application also allows users to upvote and downvote comments.

## Features

- **User Authentication**: Sign up, log in, edit user details, and log out.
- **User Profiles**: View and edit user profiles, including a list of comments made by the user.
- **Star Wars Data**: Browse and view details of Star Wars characters, films, starships, vehicles, species, and planets.
- **Comments**: Add comments to Star Wars elements, view comments, and manage comments (edit or delete).
- **Voting System**: Upvote and downvote comments.

## Technology Stack

- **Flask**: Web framework used for building the application.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Database for storing application data.
- **Flask-Bcrypt**: For password hashing and authentication.
- **Flask-DebugToolbar**: For debugging and development purposes.

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL
- A virtual environment tool like `venv` or `virtualenv`

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/star-wars-flask-app.git
   cd star-wars-flask-app
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add the following:

   ```env
   DATABASE_URL=postgresql:///star_wars
   SECRET_KEY=your_secret_key
   ```

5. **Initialize the database:**

   ```bash
   python app.py
   ```

   This will create the necessary tables and populate them with data from the Star Wars API.

6. **Run the application:**

   ```bash
   python app.py
   ```

   The application will start running on `http://127.0.0.1:5000/`.

## Application Routes

- **Home**: `/` - Displays the homepage.
- **Search**: `/search` - Allows users to search for Star Wars elements.
- **Sign Up**: `/signup` - User registration page.
- **Login**: `/login` - User login page.
- **Logout**: `/logout` - Logs out the user.
- **User Profile**: `/profile/<int:user_id>` - Displays user profile with their comments.
- **Edit User**: `/edit/<int:user_id>` - Allows users to edit their details.
- **Delete User**: `/edit/<int:user_id>/delete` - Deletes a user account.
- **Characters**: `/characters` - Lists all Star Wars characters.
- **Character Details**: `/characters/<int:person_id>` - Details of a specific character.
- **Films**: `/films` - Lists all Star Wars films.
- **Film Details**: `/films/<int:film_id>` - Details of a specific film.
- **Starships**: `/starships` - Lists all Star Wars starships.
- **Starship Details**: `/starships/<int:starship_id>` - Details of a specific starship.
- **Vehicles**: `/vehicles` - Lists all Star Wars vehicles.
- **Vehicle Details**: `/vehicles/<int:vehicle_id>` - Details of a specific vehicle.
- **Species**: `/species` - Lists all Star Wars species.
- **Species Details**: `/species/<int:species_id>` - Details of a specific species.
- **Planets**: `/planets` - Lists all Star Wars planets.
- **Planet Details**: `/planets/<int:planet_id>` - Details of a specific planet.
- **Vote Comment**: `/comment/<int:comment_id>/vote` - Upvote or downvote a comment.
- **Delete Comment**: `/comment/<int:comment_id>/delete` - Deletes a comment.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## Acknowledgments

- [Star Wars API (SWAPI)](https://swapi.dev/) for providing the Star Wars data.
- [Flask Documentation](https://flask.palletsprojects.com/) for the Flask framework documentation.

5. Make sure you use a free API and deploy your project on Heroku , so everyone can see your work!
