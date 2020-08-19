# Flask Scheduler

Simple Flask Scheduler project

## Getting Started

This project was created as a Homework for SkillFactory. Module E9. PWS-6. 

### Start using this project

What you need to do for correctly start using it?

* Clone or download my project
```commandline
git clone git@github.com:dannycrief/flask_scheduler.git
```

* Go to project folder
```
cd flask_scheduler
```
### Environments settings
* Create .env file and put code below in it
```.env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY='your-secret-key'
FLASK_APP=app/routes.py
DATABASE_URL='postgresql://user:password@localhost:5432/db-name'
PYTHONPATH=.
POSTS_PER_PAGE=3
```
### Alembic settings
* Create alembic migrations. Initialize alembic
```commandline
PYTHONPATH=. alembic init alembic
```
* Commit Changes
```commandline
PYTHONPATH=. alembic revision --autogenerate -m "initial migration" 
```
* Confirm migrations
```commandline
PYTHONPATH=. alembic upgrade head
```
* Modify alembic config in alembic.ini
```ini
sqlalchemy.url = postgresql://user:password@localhost:5432/db-name
```

### Docker settings

* Build Docker
```commandline
docker-compose build
```

* Fist of all up postgres container
```commandline
docker-compose up postgres
```

* And up all containers
```commandline
docker-compose up
```

## Author

* **[Stepan Kozurak](https://www.linkedin.com/in/stepan-kozurak-77485b16b/)**