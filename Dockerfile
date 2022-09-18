FROM python:3.9.6-slim

WORKDIR /river-health/app
COPY ./app .

WORKDIR /river-health

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py main.py

EXPOSE 8080

ENTRYPOINT ["gunicorn", "main:app", "--bind", "0.0.0.0:8080", "-w", "3", "-t", "0"]











