FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 config.wsgi:application