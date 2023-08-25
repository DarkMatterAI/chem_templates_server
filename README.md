# chem_templates_server
Docker server for chem_templates library


docker build -t chem_templates_server .
docker run -d --name test_functional -p 7861:7861 -e PORT="7861" chem_templates_server

docker run -d --name test_stateful -p 7861:7861 -e PORT="7861" -e MONGO_URI="mongodb://172.17.0.2:27017" chem_templates_server
docker run -d --name test_stateful -p 7861:7861 -e PORT="7861" -e WORKERS="32" -e MONGO_URI="mongodb://172.17.0.2:27017" chem_templates_server

docker run -d --name test -p 7861:7861 -e PORT="7861" -e WORKERS="32" chem_templates_server

uvicorn app.main:app --host 0.0.0.0 --port 7861 --workers 1 --timeout-keep-alive 120

docker exec -it {container_id} app/tests/tests-start.sh

docker-compose exec template_server app/tests/tests-start.sh

todos:
    readme
        build instructions
    api docs
    docker up overview docs