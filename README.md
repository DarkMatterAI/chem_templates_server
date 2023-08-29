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

The service is now running at port 7861, with API docs at `http://localhost:7861/docs`

# Docs

View the [docs](https://github.com/DarkMatterAI/chem_templates_server/tree/main/docs) directory for

- [Setup](https://github.com/DarkMatterAI/chem_templates_server/blob/main/docs/01%20setup.md)
- [Template API](https://github.com/DarkMatterAI/chem_templates_server/blob/main/docs/02%20template%20api.md)
- [Assembly API](https://github.com/DarkMatterAI/chem_templates_server/blob/main/docs/03%20assembly%20api.md)

