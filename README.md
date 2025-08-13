# NeXflix Database Project

## Overview
This project is a web application built with **Flask** and **MySQL** that simulates the Netflix platform's database management system. It allows for CRUD (Create, Read, Update, Delete) operations on various tables related to users, profiles, subscriptions, content, episodes, user activities, payments, payment histories, and casts.

## Table of Contents
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Available Routes](#available-routes)
- [CRUD Operations](#crud-operations)
- [Technologies Used](#technologies-used)

## Installation
## Set up a virtual environment (optional but recommended):
1.  
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. pip install -r requirements.txt

## Database Schema

This project consists of the following tables in the MySQL database:

user
profile
subscription
content
episode
user_activity
payment
payment_history
cast
The following bridge tables have also been set up to manage many-to-many relationships:

content_bridge_cast
movies_tvshows_bridge_cast
content_bridge_profile

## Setup Instructions

MySQL Database Setup:
Open MySQL Workbench or use the MySQL CLI.
Create a new database named Netflix:

1.  CREATE DATABASE Netflix;

2. USE Netflix;

source path/to/your/schema.sql;  # Replace with the actual path

## Configure the database connection in the Flask app:
Open the app.py file.
Set your MySQL credentials in the connection string:


1. mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="Netflix"
)

## Set the Flask secret key:

2. app.config['SECRET_KEY'] = 'your_secret_key'

## Running the Application
Start the Flask app:
1. python app.py
2. Open the application in a browser:
    Go to http://127.0.0.1:5000/.

## Available Routes

## Route	                                            Description
/	                                                Homepage with table list
/users	                                            View all users
/add_user	                                        Add a new user
/update_user/<id>	                                Update user details
/profiles	                                        View all profiles
/add_profile	                                    Add a new profile
/subscriptions	                                    View all subscriptions
/add_subscription	                                Add a new subscription
/contents	                                        View all content
/add_content	                                    Add new content
/episodes	                                        View all episodes
/add_episode	                                    Add a new episode
/user_activity	                                    View all user activities
/payments	                                        View all payments
/add_payment	                                    Add a new payment
/payment_history	                                View payment history
/add_payment_history	                            Add payment history
/casts	                                            View all cast records
/add_cast	                                        Add a new cast record


## CRUD Operations

The following CRUD operations are available for each table:

Create: Add a new entry to the table.
Read: View all entries from the table.
Update: Modify existing entries.
Delete: Remove entries from the table.
Each operation is accessible through its respective route as mentioned in the Available Routes section.

## Technologies Used

Backend: Python, Flask, MySQL
Frontend: HTML, Jinja2 Templates, Bootstrap
Database: MySQL
Libraries: Flask-WTF, MySQL Connector, Jinja2

## Troubleshooting

### ImportError: No module named 'mysql.connector'

If you see an error like:

```
ModuleNotFoundError: No module named 'mysql.connector'
```

You need to install the MySQL connector for Python. Run this command in your terminal:

```bash
pip install mysql-connector-python
```

If you are using a virtual environment, make sure it is activated before running the above command.



