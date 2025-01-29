FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt update && apt install unzip nmap wget curl
RUN pip install --no-cache-dir -r requirements.txt
RUN unzip chall.zip
EXPOSE 5000
RUN rm Dockerfile docker-compose.yml requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]
