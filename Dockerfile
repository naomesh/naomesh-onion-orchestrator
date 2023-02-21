FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4200/tcp

CMD [ "python", "./src/main.py" ]
