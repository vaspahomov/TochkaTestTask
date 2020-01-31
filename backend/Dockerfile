FROM python:3.8

WORKDIR /app

COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

EXPOSE 5000
COPY ["src/", "./"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]