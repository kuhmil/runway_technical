FROM python:3.9

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "runway_technical.main:app", "--host", "0.0.0.0", "--port", "80"]