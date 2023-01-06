FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN PIP install --no-cache-dir -r requeriments.txt

CMD ["gunicorn", "--bind" "0.0.0.0:5000", "app:app"]