# Setup Instructions

The `chem_templates_server` service can run as a standalone service, or be connected to an 
optional [MongoDB](https://www.mongodb.com/) backend to support CRUD operations 
and saving templates. The instructions below show several different ways of configuring the service.

## Quickstart

The simplest way to start the service is with `docker-compose`. This builds both the template 
server and the MongoDB backend. 

Note you may wish to edit the `WORKERS` env variable in `docker-compose.yml` if you want 
the service to use multiple cores.

```
git clone https://github.com/DarkMatterAI/chem_templates_server

cd chem_templates_server

docker-compose up -d --build

docker-compose exec template_server app/tests/tests-start.sh
```

## Connect to existing MongoDB database

It is also possible to build just the template server and connect it to an existing MongoDB database

```
docker pull dmaichem/chem_templates_server

docker run -d \
     -p $PORT:$PORT \
     -e PORT=$PORT \
     -e HOST=$HOST \
     -e WORKERS=$WORKERS \
     -e TIMEOUT=$TIMEOUT \
     -e MONGO_URI=$MONGO_URI \
     -e MONGO_DB_NAME=$MONGO_DB_NAME \
     dmaichem/chem_templates_server

docker exec -it {container_id} app/tests/tests-start.sh
```

## Standalone service

The template server can be used as a purely functional server without a MongoDB backend

```
docker pull dmaichem/chem_templates_server

docker run -d \
     -p $PORT:$PORT \
     -e PORT=$PORT \
     -e HOST=$HOST \
     -e WORKERS=$WORKERS \
     -e TIMEOUT=$TIMEOUT \
     dmaichem/chem_templates_server

docker exec -it {container_id} app/tests/tests-start.sh
```

## Build from source

It is also possible to build the service from the repo

```
git clone https://github.com/DarkMatterAI/chem_templates_server

cd chem_templates_server

docker build -t chem_templates_server .

docker run -d \
     -p $PORT:$PORT \
     -e PORT=$PORT \
     -e HOST=$HOST \
     -e WORKERS=$WORKERS \
     -e TIMEOUT=$TIMEOUT \
     chem_templates_server

docker exec -it {container_id} app/tests/tests-start.sh
```

