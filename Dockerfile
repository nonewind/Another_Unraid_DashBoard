FROM python:3.9.16

# Path: .DockerFile

WORKDIR /anthor_dashborad/

COPY . /anthor_dashborad/

# COPY /requirements.txt /anthor_dashborad/

RUN pip install -r requirements.txt

# COPY . /anthor_dashborad/
# 初始化
CMD ["/bin/bash", "/anthor_dashborad/docker-entrypoint.sh"]