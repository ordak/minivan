# start by pulling the python image
# FROM python:3.8-alpine
FROM ubuntu:latest

# install the dependencies and packages in the requirements file
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY requirements.txt requirements.txt


# RUN apt-get install python-pip3

RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY . .

# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

CMD ["torserv.py" ]
