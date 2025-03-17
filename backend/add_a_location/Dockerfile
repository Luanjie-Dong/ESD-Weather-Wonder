FROM python:3.9-slim

WORKDIR /add_a_location

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5010

CMD ["python", "add_a_location.py"]