FROM python:3.9-alpine

WORKDIR /opt/app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
    && pip install -r requirements.txt \
    && apk del .build-deps

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]
