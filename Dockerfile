FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["sh", "-c", "gunicorn --workers=4 --bind=0.0.0.0:${FLASK_RUN_PORT} --timeout=300 run:app"]