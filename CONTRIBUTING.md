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

## URL to setup base environment of Insomnia to hit endpoints locally

```
"url":"http://127.0.0.1:5005"
```