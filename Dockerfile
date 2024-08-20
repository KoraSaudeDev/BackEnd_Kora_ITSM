FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]