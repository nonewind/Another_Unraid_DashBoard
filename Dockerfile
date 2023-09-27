FROM python:3.9.16

# Path: .DockerFile

WORKDIR /App/

COPY /requirements.txt /App/

RUN pip install -r requirements.txt


COPY . /App/

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["python", "production_run.py"]
