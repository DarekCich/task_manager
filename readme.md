# Api z wykorzystaniem Django Rest Framework

## Uruchomienie 

### Należy stworzyć kontenery dockerowe
```bash
docker-compose up --build
```
### Następnie migrujemy aplikacje Django
np przy użyciu  
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Używanie

### Aplikacja web

Aplikację można uruchomić pod adresem

```
http://localhost:8000/web/tasks/
```

### API

Przykładowe zapytania podane w pliku 
```
REST_API_DRF.postman_collection.json
```
