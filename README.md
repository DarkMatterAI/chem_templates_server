# chem_templates_server

`chem_templates_server` is a containerized server running the 
[chem_templates](https://github.com/DarkMatterAI/chem_templates) library. The container runs as a
standalone service, and can optionally be connected to a [MongoDB](https://www.mongodb.com/) 
instance to enable CRUD operations and persistent storage of template schemas

# Quickstart

To start, clone the repo and build with `docker-compose`.

```
git clone https://github.com/DarkMatterAI/chem_templates_server

cd chem_templates_server

docker-compose up -d --build
```

The service is now running at port 7861



todos:
    readme
        reduce to docker compose install for brevity
    docs
        installation
            more detailed instal info
        api docs
