FROM python:3.7.5-stretch

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]