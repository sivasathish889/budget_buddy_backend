FROM python:3.13.7
 
WORKDIR /app
 
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 
 
COPY requirements.txt  /app/requirements.txt
 
RUN pip install -r requirements.txt
 
COPY . /app/
 
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
