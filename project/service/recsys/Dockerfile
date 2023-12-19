FROM python:3.11

COPY . /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

CMD ["python", "app.py"]
