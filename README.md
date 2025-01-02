# Web Platform - Signup, Login, and Profile

This project is focused on developing a web platform with **Signup**, **Login**, and **Profile** pages. The goal is to provide users with a simple, secure, and efficient way to sign up, log in, and manage their personal profiles.

## Features

- **Signup Page**: Allows users to create an account by entering details like email, password, and agreeing to terms.
- **Login Page**: Allows users to log in to their account using credentials.
- **Profile Page**: Displays user details and allows users to update their information.

## Technologies Used

- **Python**: Backend development.
- **Flask**: Web framework to build the web application.
- **SQLAlchemy**: ORM (Object-Relational Mapping) for managing database with SQLite.
- **SQLite3**: Database for storing user information.
- **HTML/CSS**: For frontend pages.
- **JavaScript**: For dynamic page elements and client-side validation.

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/RohitSingh-04/f-ecom-team1.git
   
2. **flask db init is used to initialize the migration**:
   ```bash
      flask db migrate
   ```
   >above command is used to create the migration -m flag is used with this command to add the message for example - 
   ```bash
      flask db migrate -m "Initial migration"
   ```

3. **upgrade the database**:
   
   ```bash
      flask db upgrade
   ```
   >the above command is used to apply the migration

4. **Downgrade the DataBase** 
    
   ```bash 
   flask db downgrade
   ```
   
   > the above command is used to revert the migration