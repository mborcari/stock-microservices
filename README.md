**Django stocks microservices**

Is a Django microservices project about Brazilian stocks.

**Stack of project:**

- Use pyenv and virtualenv for management environment;
- Docker and Docker-compose;
- Django, DjangoRest, Postgre, Pike, RabbitMq;


You will need install git, heroku and docker CLI.

Login in Heroku and Docker in console.

```
heroku login
heroku container: login
```
To aplication works, is need:

- 1x stock microservices. (https://github.com/mborcari/stock_microservices)
- 2x stock etl microservices (https://github.com/mborcari/stock_etl_microservices)
- 1x Postgres database instance.
- 1x RabbitMQ instance.

Here, you will create main microsservices, database and rabbitmq. 

**Warning: Remember change tag "yourname" in this readme!.

First, create the main stock microservices:

  **Heroku commands to stock microservices:**
  
  Create app container:
  ```
  heroku create stock-ms-yourname
  ```

  Create add-on database postgres:
  ```
  heroku addons:create heroku-postgresql:hobby-dev -a stock-ms-pytrader
  ```

  Create add-on Rabbitmq:
  ```
  heroku addons:create cloudamqp:lemur -a stock-ms-pytrader
  ```

  You will need get dabatabase and RabbitMQ credencials on Heroku site after create instance.
  
  Now, before create and deploy image, create .env file on root project. Set this variables:
  
  ```
  SECRET_KEY=<generate your key>
  DEBUG=True
  ALLOWED_HOSTS_DJANGO=127.0.0.1, localhost, .herokuapp.com
  DJANGO_SETTINGS_MODULE=stocks_microservices.settings

  #URL TO ACCESS DB
  DATABASE_URL=<get on heroku site after create postgres instance>

  #RABBITMQ
  RABBITMQ_KEY=get on heroku site after create RabbiwMQ instance>
  ```
 
  Now, build image and deploy on Heroku app:
  ```
  docker build -f Dockerfile-heroku -t img_stock_ms .
  docker tag img_stock_ms registry.heroku.com/ stock-ms-yourname/web
  docker push registry.heroku.com/ stock-ms-yourname/web
  heroku container:release web -a  stock-ms-yourname
  heroku ps:scale web=1 -a stock-ms-yourname
  ```

  To see if the application ran, see log:
  ```
  heroku logs --tail -a  stock-ms-yourname
  ```
  
  If you need restart:
  ```
  heroku ps:restart web=1 -a stock-ms-yourname
  ```

**Repeat process to stock queue microservices:**

  Create app
  ```
  heroku create stock-ms-queue-yourname
  ```

  Build and deploy image to Heroku
  ```
  docker build -f Dockerfile-heroku-queue -t img_stock_ms_queue .
  docker tag img_stock_ms_queue registry.heroku.com/stock-ms-queue-yourname/worker
  docker push registry.heroku.com/stock-ms-queue-yourname/worker
  heroku container:release worker -a stock-ms-queue-yourname
  heroku ps:scale worker=1 -a stock-ms-queue-yourname
  heroku logs --tail -a stock-ms-queue-yourname
  ```


If you want, in you machine or inside heroku container, execute dataset_example/load_data.py (change const URL_BASE):
