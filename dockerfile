# Dockerfile

# Używamy oficjalnego obrazu Pythona z Django
FROM python:3.8

# Ustawiamy zmienną środowiskową dla Pythona, aby nie pokazywał polecenia 
# pythonu do wpisywania kodu (python -i)
ENV PYTHONUNBUFFERED 1

# Tworzymy i ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki z projektu do katalogu roboczego
COPY . /app/

# Instalujemy zależności
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Wykonujemy migracje podczas budowania obrazu
