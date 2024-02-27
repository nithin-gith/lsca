FROM python:3.8-slim-buster

WORKDIR /project

COPY . /project/

RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]