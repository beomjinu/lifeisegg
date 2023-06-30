FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application
ENTRYPOINT python manage.py migrate --noinput