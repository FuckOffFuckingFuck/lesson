FROM python:3.12.5

WORKDIR /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

COPY . .

CMD [ "python", "-m", "src.main" ]
