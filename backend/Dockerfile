FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY docusecure docusecure
COPY docs docs
COPY accounts accounts
COPY search search
COPY extapi extapi
COPY templates templates
COPY static static
COPY manage.py .

COPY logs logs

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
