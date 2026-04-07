Build and push the Docker image, then tag it with 24ds3000006.

Replace <USER> and <REPO> with your Docker Hub username and repo name.

Build:
```powershell
docker build -t <USER>/<REPO>:latest .
```

Tag with the required tag:
```powershell
docker tag <USER>/<REPO>:latest <USER>/<REPO>:24ds3000006
```

Login to Docker Hub:
```powershell
docker login
```

Push both tags:
```powershell
docker push <USER>/<REPO>:latest
docker push <USER>/<REPO>:24ds3000006
```

Docker Hub repository URL (no secret):
https://hub.docker.com/repository/docker/<USER>/<REPO>/general

If you hit rate limits or need to include a token, append the optional query:
https://hub.docker.com/repository/docker/<USER>/<REPO>/general?secret=$TOKEN&identifier=$USER
