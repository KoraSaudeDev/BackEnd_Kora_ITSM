FROM python:3.9

WORKDIR /app

COPY . .

COPY ./nwrfcsdk /usr/local/sap/nwrfc

ENV SAPNWRFC_HOME=/usr/local/sap/nwrfc
ENV LD_LIBRARY_PATH=/usr/local/sap/nwrfc/lib:$LD_LIBRARY_PATH

RUN apt-get update && \
    apt-get install -y build-essential libxml2-dev libxslt1-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install cython==0.29.21

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["sh", "-c", "gunicorn --workers=4 --bind=0.0.0.0:${FLASK_RUN_PORT:-5000} --timeout=300 --log-level=debug --access-logfile=- --error-logfile=- run:app"]