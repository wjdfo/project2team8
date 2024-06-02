FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000