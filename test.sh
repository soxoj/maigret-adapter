#!/bin/bash
./run.py & sleep 1

PORT=8080

[[ `curl localhost:$PORT -s` == "Maigret adapter v0.0.1" ]] && echo 'valid mainpage' || echo 'invalid mainpage'
[[ `curl localhost:$PORT/check/service/username -s` == '{"maigret-adapter": "0.0.1", "error": "Unsupported service"}' ]] && echo 'valid check result' || echo 'invalid check result' 
curl http://localhost:$PORT/sites/test_service
python3 -m maigret --db http://localhost:$PORT/sites/test_service found notfound
curl localhost:$PORT/exit
