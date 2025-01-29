FROM python:3.11.9-bookworm

WORKDIR /app
COPY app/* ./
RUN pip3 install -r requirements.txt
EXPOSE 12345

CMD ["python3", "-u", "./server.py"]