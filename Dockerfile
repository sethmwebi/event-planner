FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
