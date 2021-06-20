FROM python:3

WORKDIR /usr/py_code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "./ttn-listener_v0.2.py" ]
