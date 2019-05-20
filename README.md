# Pur Beurre - Project 8 OpenClassrooms

### How to use

First create a postgreSQL Database with the name / username & password of your choosing.

Then you will need to create a ".env" file in the project root :

```dotenv
ENV = PRODUCTION  # or anythings else if dev
SECRET_KEY = "your_secret_key"
DB_NAME = database_name
DB_USERNAME = database_username
DB_PASSWORD = database_password
# pytest tests
DJANGO_SETTINGS_MODULE = your_project.settings
```

Once its done, install the requirements.txt (following command should work)
```commandline
pip install -r requirements.txt
```

After that, you can run the server with those commands
```commandline
./manage.py migrate
./manage.py runserver
```

#### Live Demo

A live demo is available here : https://purbeurre-coa.herokuapp.com/ .