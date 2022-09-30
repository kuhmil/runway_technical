FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./runway_technical /code/runway_technical

CMD ["uvicorn", "runway_technical.main:app", "--host", "0.0.0.0", "--port", "80"]