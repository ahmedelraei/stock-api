FROM python:3.10.6-alpine
WORKDIR /
RUN pip3 install fastapi uvicorn fastapi-mqtt requests paho-mqtt
EXPOSE 8000