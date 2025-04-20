FROM python:alpine

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py", "--host=0.0.0.0", "--port=3000" ]