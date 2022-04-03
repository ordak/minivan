# start by pulling the python image
# FROM python:3.8-alpine
FROM ubuntu:latest

# install the dependencies and packages in the requirements file
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential

# switch working directory
WORKDIR /app

# install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy everything from the local file to the image
COPY . .

# run the ding dang thing
CMD ["python3", "torserv.py" ]
