From python:3.12-slim

WORKDIR /usr/src/core

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

#COPY ./app .
#
#CMD ["fastapi","dev","--host","0.0.0.0","--port","8000"]
# docker build -t myimage .
# docker run -d --name mycontainer -p 8000:8000 myimage
# docker pull docker.arvancloud.ir/python:3.12-slim

