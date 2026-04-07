@echo off
ngrok http 11434 --response-header-add "X-Email: 24ds3000006@ds.study.iitm.ac.in" --response-header-add "Access-Control-Expose-Headers: *" --response-header-add "Access-Control-Allow-Headers: Authorization,Content-Type,User-Agent,Accept,Ngrok-skip-browser-warning"
