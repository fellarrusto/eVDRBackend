FROM python:3.9-alpine

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY start.sh .
RUN chmod +x start.sh

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["start.sh"]
