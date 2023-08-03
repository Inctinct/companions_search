To start the application you need:
  1. git clone https://github.com/Inctinct/companions_search/
  2. pip install -r requirements.txt
  3. python manage.py makemigrations
  4. python manage.py migrate
  5. python manage.py createsuperuser
  6. python manage.py runserver

To start the application with docker:
 1. git clone https://github.com/Inctinct/companions_search/
 2. docker-compose build
 3. docker-compose up -d
 4. docker-compose run web python manage.py makemigrations
 5. docker-compose run web python manage.py migrate
 6. docker-compose run web python manage.py createsuperuser
