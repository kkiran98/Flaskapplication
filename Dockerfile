
FROM python:3.8


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade Flask Werkzeug


EXPOSE 8010 80


CMD ["python", "app.py"]

