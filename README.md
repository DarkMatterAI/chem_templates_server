# chem_templates_server

`chem_templates_server` is a containerized server running the 
[chem_templates](https://github.com/DarkMatterAI/chem_templates) library. The container runs as a
standalone service, and can optionally be connected to a [MongoDB](https://www.mongodb.com/) 
instance to enable CRUD operations and persistent storage of template schemas

# Quickstart

## Standalone Service

The standalone service is available on Docker Hub

```
docker pull dmaichem/chem_templates_server

docker run -d \
     -p $PORT:$PORT \
     -e PORT=$PORT \
     -e HOST=$HOST \
     -e WORKERS=$WORKERS \
     -e TIMEOUT=$TIMEOUT \
     dmaichem/chem_templates_server
```

To build from source

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
```

## Stateful Service with MongoDB Connection

The easiest way to start the stateful service is to use the supplied `docker-compose.yml`. This 
will build the `chem_templates_server` container and a MongoDB container.

```
git clone https://github.com/DarkMatterAI/chem_templates_server

cd chem_templates_server

docker-compose up -d --build
```

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
```

## Test Build

To test the build, run 

```
docker exec -it {container_id} app/tests/tests-start.sh
```

or, if you used `docker-compose`

```
docker-compose exec template_server app/tests/tests-start.sh
```

todos:
    readme
        build instructions
    api docs
    docker up overview docs