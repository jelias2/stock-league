# **Stock League**

Fantasy Football but for stock trading

## **Deploy**

> Install [**Docker**](https://docs.docker.com/get-docker/)

### **Easy Way** :grin: (use `docker-compose`)

```bash
$ docker-compose up -d --build
Creating network "stock-league_default" with the default driver
Building flask
Step 1/10 : FROM python:3.9.1-slim-buster
 ---> 8c84baace4b3
Step 2/10 : WORKDIR /usr/src/app
 ---> Using cache
 ---> da6512e300e3
Step 3/10 : ENV PYTHONDONTWRITEBYTECODE 1
 ---> Using cache
 ---> c85d2bc62141
Step 4/10 : ENV PYTHONUNBUFFERED 1
 ---> Using cache
 ---> 2306875a8b7d
Step 5/10 : RUN pip install --upgrade pip
 ---> Using cache
 ---> 187a71f8e439
Step 6/10 : COPY ./requirements.txt /usr/src/app/requirements.txt
 ---> Using cache
 ---> 958b8af8452b
Step 7/10 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> f87f848e1d3a
Step 8/10 : COPY . /usr/src/app/
 ---> Using cache
 ---> d64bfae89d24
Step 9/10 : EXPOSE 5000
 ---> Using cache
 ---> 740e6609445d
Step 10/10 : ENTRYPOINT [ "sh", "/usr/src/app/run-flask.sh" ]
 ---> Using cache
 ---> c2e65d5c5a7f

Successfully built c2e65d5c5a7f
Successfully tagged stock-league_flask:latest
Creating stock-league_flask_1 ... done
```

### **Hard Way** :sweat:

1. Build the Docker Image for `Stock League` Flask API

   ```bash
   docker build -t "stocks_league_flask" services/stock_league
   ```

2. List the docker image
   > Output should be similar

   ```bash
    $ docker images
    REPOSITORY                                                   TAG                 IMAGE ID       CREATED          SIZE
    stocks_league_flask                                          latest              18ba6ac7a6ff   4 minutes ago    307MB
   ```

3. Deploy the Flask API

   ```bash
   $ docker run -d -p 5000:5000 --name "stock_league_api" stocks_league_flask
   5f170ba24b661fa83a4ef2c7e9e8727c0d9922f53f6bb4ca46b0765008a80922
   
   $ docker ps
   CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                    NAMES
   5f170ba24b66   stocks_league_flask   "sh /usr/src/app/run…"   19 seconds ago   Up 18 seconds   0.0.0.0:5000->5000/tcp   stock_league_api
   ```

## **Use**

1. Install [Postman](https://www.postman.com/downloads/)

2. Import postman collection [`Stocks_League.postman_collection.json`](./Stocks_League.postman_collection.json)

## **CleanUp**

> [Docker Cheatsheet](https://www.docker.com/sites/default/files/d8/2019-09/docker-cheat-sheet.pdf)

1. Shutdown all containers and delete

   ```bash
   $ docker-compose down -v
   Stopping stock-league_flask_1 ... done
   Removing stock-league_flask_1 ... done
   Removing network stock-league_default
   ```

2. Shutdown the Flask API Server in Docker

   ```bash
   docker stop stock_league_api 
   ```

3. Delete the Container

   ```bash
   docker rm stock_league_api 
   ```
