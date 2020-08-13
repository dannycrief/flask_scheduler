```dockerfile
docker run --rm  --name postgres-scheduler -e POSTGRES_PASSWORD=211217ns -d -p 5432:5432 postgres:latest
docker exec -it flask-db psql -U postgres -c "create database weather_forecast_dev"
```