# chem_templates_server
Docker server for chem_templates library


docker build -t chem_templates_server .
docker run -d --name test -p 7861:7861 -e PORT="7861" -e WORKERS="10" chem_templates_server

uvicorn app.main:app --host 0.0.0.0 --port 7861 --workers 1 --timeout-keep-alive 120 --reload
