FROM python:3.13

WORKDIR /shop/backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]