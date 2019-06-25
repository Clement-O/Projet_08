# Pur Beurre - Project 8 OpenClassrooms

### How to use

First create a postgreSQL Database with the name / username & password of your choosing.

Then you will need to create a ".env" file in the project root :

```dotenv
ENV = DEV_OR_ANYTHING_ELSE
SECRET_KEY = "your_secret_key"
DB_NAME = database_name
DB_USERNAME = database_username
DB_PASSWORD = database_password
DB_HOST = database_host

# (optional) If ENV = PRODUCTION add this line if you want to monitorise the project
# SENTRY_DSN = your_sentry_dsn

# On Heroku, set these variables as 'Config Vars'. ENV should then be set to 'HEROKU'
```

Once its done, install the requirements.txt (following command should work)
```commandline
pip install -r requirements.txt
```

After that, you can run the server with those commands 
(don't forget to change the ALLOWED_HOSTS in settings)
```commandline
./manage.py migrate
./manage.py runserver
```

#### Live Demo

A live demo is available here : 
- https://purbeurre-coa.herokuapp.com/
- http://68.183.47.65/