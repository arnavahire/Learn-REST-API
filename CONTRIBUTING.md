## How to run Dockerfile locally

This is how the dockerfile should look like if you want to run it locally.

```
FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["flask", "run", "--host", "0.0.0.0"]
```

In order to build and run the docker image locally run the following commands

```
docker build -t <image_name> .
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" <image_name>

Example:
docker build -t rest-api-flask-python .     
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-api-flask-python
```

## URL to setup base environment of Insomnia to hit endpoints

### Locally
When you setup the docker to listen on 5005 port use the following port.
Update this in Base Environment section of Insomnia and you should be good to go.

```
"url":"http://127.0.0.1:5005"
```
### Render.com
After creating account, logging in and configuring the project, once rendered it will create a url for you. This is the one for Stores Rest API setup. 
Update this in Base Environment section of Insomnia and you should be good to go.
```
"url":"https://learn-rest-api-5rsi.onrender.com"
```

## Connecting to database client locally. 
You can connect to a local database client such as DBeaver when you create a .env file and specify DATABASE_URL within it which is nothing but database connection string usually obtained while setting up the database. You can use the docker-compose file to decide the postgreSQL version, user and password and can use .env file where you can update DATABASE_URL. Refer an example in .env.example file in this project. If .env is not used, by default we are using sqlite db as configured in apps.py

```
docker compose up --build --force-recreate --no-deps db
```
to setup the db locally.

However currently we are directly connecting to the db locally or we are using render.com to host our application.

# Refer this e-book for more details
https://rest-apis-flask.teclado.com/docs/course_intro/