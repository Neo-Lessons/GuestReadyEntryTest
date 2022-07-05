# pull official base image
FROM python:3.9.6-alpine

EXPOSE 3000

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
     && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# prepare script
RUN sed -i 's/\r$//g' /usr/src/app/run_build_docker.sh
RUN chmod +x /usr/src/app/run_build_docker.sh

# run script
ENTRYPOINT ["/usr/src/app/run_build_docker.sh"]
