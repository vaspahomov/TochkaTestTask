FROM python:3.8

WORKDIR /app

COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

EXPOSE 5000
COPY ["src/", "./"]

CMD ["python3", "app.py"]