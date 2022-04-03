# Running

  * Standard stuff:
     * _(recommended to use virtualenv)_
    ```
    pip install -r requirements.txt
    python torserv.py
    ```
  * Endpoints:
     * _if running locally on port 8888_
     * [main](http://localhost:8888)
     * [input only](http://localhost:8888/inputOnly)
     * [sensors](http://localhost:8888/sensors)

# Dockerization

  * This lives in the `minivan` repository at [DockerHub][http;//hub.docker.com] for user `wpgalle3`
  * After changing code
      * To build Docker image:
        ```
        docker build . -t wpgalle3/minivan
        ```
      * To push to Docker Hub:
        ```
        docker login --username wpgalle3 --password-stdin
        docker push wpgalle3/minivan
        ```
  * To run locally (containerized) on Linux:
    ```
    docker run -p 8888:8888 wpgalle3/minivan:latest
    ```
  * Running on Windows
      * Install Docker on Windows [instructions](https://docs.docker.com/desktop/windows/install/)
      * To run container on Windows: (in Terminal):
        ```
        docker pull wpgalle3/minivan:latest
        docker run --name minivan -p 8888:8888 wpgalle3/minivan:latest
        ```
      * To stop container on Windows: (in Terminal):
        ```
        docker stop minivan
        docker rm minivan
        ```
# Backlog

  * add "changed" flags for all UI fields, esp. accumulated
      * **DONE** model in DSs
      * pass in handlers
      * utilize in JS
  * make frontend pass button indices not IDs
  * make events nonconsumable
  * propagate button func changes between windows

