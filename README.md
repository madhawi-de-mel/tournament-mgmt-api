**Tournament Management System API**

Execute following commands to load data to DB

`python3 -m venv env`

`source env/bin/activate`  # On Windows use `env\Scripts\activate`

`python manage.py migrate`

`python manage.py makemigrations management_app`

`python manage.py migrate management_app`

`python manage.py loaddata tournament.json`
