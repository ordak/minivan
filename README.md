# Dockerization

  * This lives in the `minivan` repository at [DockerHub][http;//hub.docker.com] for user `wpgalle3`

  * To build Docker image:
```
docker build . -t wpgalle3/minivan
```

  * To push to Docker Hub
```
docker login --username wpgalle3 --password-stdin
docker push wpgalle3/minivan
```
