FROM python:3

WORKDIR /usr/src/app

COPY . .

# COPY /requirements.txt .

RUN pip install -r requirements.txt

# COPY /manage.py .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000