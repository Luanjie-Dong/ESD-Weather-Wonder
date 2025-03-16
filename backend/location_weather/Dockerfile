FROM python:3.13.2-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /location_weather

COPY main.py .
COPY .env .

EXPOSE 5003

CMD ["python", "main.py"]