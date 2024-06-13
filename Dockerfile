FROM python:3.11-alpine

WORKDIR /application

RUN python -m pip install --upgrade pip

COPY requirements.txt /application

RUN pip install -r requirements.txt

COPY . /application

CMD ["python", "liq_rates.py"]