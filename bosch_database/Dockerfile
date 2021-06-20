FROM python:3

WORKDIR /usr/py_code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]
