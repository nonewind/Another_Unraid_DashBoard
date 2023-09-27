FROM python:3.9.16

# Path: .DockerFile

WORKDIR /anthor_dashborad/

COPY . /anthor_dashborad/



RUN pip install -r requirements.txt

ENV UNRAID_HOST_TYPE=0
ENV UNRAID_HOST=192.168.0.1
ENV UNRAID_USERNAME=root
ENV UNRAID_PASSWORD=123

# 初始化
CMD ["/bin/bash", "/anthor_dashborad/docker-entrypoint.sh"]