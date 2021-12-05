**Django project microservices**

Is a Django microservices project about stocks. **Under development.**

**Stack used:**

- Use pyenv and virtualenv for management environment;
- Stack Django, DjangoRest, Postgre, Pike, RabbitMq;
- Docker and Docker-compose.

You will need install git, heroku and docker CLI.

Login in Heroku and Docker in console.
```
heroku login
heroku container: login
```

**Heroku commands to stock microservices:**
- Change stock-ms-pytrader to you appname

Create app and database
```
heroku create stock-ms-pytrader
heroku addons:create heroku-postgresql:hobby-dev -a stock-ms-pytrader
```

Build image and deploy on Heroku app
```
docker build -f Dockerfile-heroku -t img_stock_ms .
docker tag img_stock_ms registry.heroku.com/stock_ms/worker
docker push registry.heroku.com/stock_ms/worker
heroku container:release worker -a stock_ms
heroku logs --tail -a stock_ms
```


**Repeat process to stock queue microservices:**
Create app
```
heroku create stock_ms_queue_heroku
```
Build and deploy image to Heroku
```
docker build -f Dockerfile-heroku-queue -t img_stock_ms_queue .
docker tag img_stock_ms_queue registry.heroku.com/stock_ms_queue/worker
docker push registry.heroku.com/stock_ms_queue/worker
heroku container:release worker -a stock_ms_queue
heroku logs --tail -a stock_ms_queue
```