#!/bin/bash
./run.py & sleep 1

PORT=8080

[[ `curl localhost:$PORT -s` == '{"maigret-adapter": "0.0.1", "usage": "/check/{service}/{site}/{identifier}", "services": ["test_service", "mailcat"]}' ]] && echo 'valid mainpage' || echo 'invalid mainpage'
[[ `curl localhost:$PORT/check/service/site/username -s` == '{"maigret-adapter": "0.0.1", "error": "Unsupported service"}' ]] && echo 'valid check result' || echo 'invalid check result'
curl http://localhost:$PORT/sites/test_service
python3 -m maigret --db http://localhost:$PORT/sites/test_service found notfound
curl localhost:$PORT/exit
