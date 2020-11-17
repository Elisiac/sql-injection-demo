# SQL injection demo

![Header SQL injection](./src/app/static/img/header.png "SQL injection Demo header")

A minimal python-flask web application to demonstrate SQL injection.

_Note: This demo is written in two parts and shows a very simple SQL injection as well as a more advance one._ 

# Quick start

To run the demo on your own machine, execute the following:
```bash
# Clone this repository
git clone git@github.com:Elisiac/sql-injection-demo.git
cd sql-injection-demo

# Setup a virtual environment
python3 -m venv ./venv/
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Open file ./src/config.py and ./src/init_db.py and replace the <secrets> with your own values

# Initialize the database
./src/init_db.py

# Run the application
./src/run.py
```

You should now be able to access the application at  http://127.0.0.1:5000/login 

# How it is built

The service is using a small SQlite datatabase with a web python-flask web server on top to serve pages to the user. 

The database model is described in the [`models.py`](./src/app/models.py) file where we create two tables: one for `users` and one for their corresponding bank `records` (or transactions). 

Each contain a number of columns that we will use to store information for our app.

The pages themselves are served from the [`views.py`](./src/app/views.py) file where we created a `login`, and `logout` and an `index` page (that you can only see when logged in). 

The HTML is contained into the [`templates`](./src/app/templates) folder and uses JINJA2 as a text processor. This allows macros as well as avoid repetition in the HTML code. [`static`](./src/app/static) contains resources like CSS (to make our page look pretty) as well as other resources like images.

We invite you to read the code itself as there is a lot of comments helping you understand what is happening.

# Scenario

You are a client at Great Bank. The best bank of the country, or at least it seems so. But you are not here to play around, you want big money and for that, you need to steal the admin password of the bank and transfer a lot of money to yourself.

The admin has a strong password and you cannot guess it. You have to somehow either bypass it entirely or steal it.

In part 1, we show how to bypass the login and in part 2, we show how to extract the password from the database directly.

Use the login `alice` and `1234` as a password to login into the application.

Please refer to the [`views.py`](./src/app/views.py) file to start the demo.




