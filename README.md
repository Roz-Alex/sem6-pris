# PRIS labs for 6th semester from Rozanov Alex

## Lab 1

### Цель

Ознакомиться с Kubernetes (k8s), развернуть PostgreSQL сервер с использованием minikube, настроить мониторинг с помощью Prometheus и Grafana.

### Задачи

1.  Развернуть minikube.
2.  Создать Deployment для PostgreSQL.
3.  Установить количество подов на 3.
4.  Добавить Metrics Server.
5.  Настроить Horizontal Pod Autoscaler (HPA).
6.  Настроить Prometheus и Grafana, настроить дашборды в Grafana.

### Инструкция

#### 1. Развертывание minikube

1.  Запустите кластер minikube:
    ```bash
    minikube start
    ```

#### 2. Создание Deployment для PostgreSQL и установка количества подов

1.  Создайте YAML-файл для Deployment, `pdeployment.yaml`. Для корректной работы нескольких экземпляров PostgreSQL требуется настройка репликации или StatefulSet. Ниже пример простого Deployment'а с 3 репликами одного standalone сервера (они не будут знать друг о друге):
    ```yaml
    metadata:
	  name: my-postgres-deployment
	spec:
	  replicas: 3
	  selector:
	    matchLabels:
	      app: my-postgres
	  template:
	    metadata:
	      labels:
	        app: my-postgres
	    spec:
	      containers:
	      - name: my-postgres
	        image: my-postgres:v1
	        ports:
	        - containerPort: 5432
	          name: postgres
	        env:
	        - name: POSTGRES_DB
	          value: mobile_dev
	        - name: POSTGRES_USER
	          value: entityfrm
	        - name: POSTGRES_PASSWORD
	          value: pP3VJsoAcX2q
	        volumeMounts:
	        - name: postgres-data
	          mountPath: /var/lib/postgresql/data
	      volumes:
	      - name: postgres-data
	        persistentVolumeClaim:
	          claimName: postgres-pvc
    ```

1.1 Добавьте Dockerfile
	```
	ENV POSTGRES_DB=mobile_dev
	ENV POSTGRES_USER=entityfrm
	ENV POSTGRES_PASSWORD=pP3VJsoAcX2q

	COPY init.sql /docker-entrypoint-initdb.d/

	VOLUME /var/lib/postgresql/data

	EXPOSE 5432
	```

1.2 Создайте файл init.sql (опционально, если есть чем заполнить БД)

1.3 Добавьте файл pvc.yaml

	```
	metadata:
	  name: postgres-pvc
	spec:
	  accessModes:
	    - ReadWriteOnce
	  resources:
	    requests:
	      storage: 10Gi
	```


2.  Примените конфигурацию:
    ```bash
    kubectl apply -f postgres-deployment.yaml
    ```
3.  Проверьте статус:
    ```bash
    kubectl get deployments
    kubectl get pods
    kubectl get services
    ```

#### 3. Добавление Metrics Server

1.  Включите Metrics Server как addon minikube:
    ```bash
    minikube addons enable metrics-server
    ```
2.  Проверьте под:
    ```bash
    kubectl get pods -n kube-system | grep metrics-server
    ```
3.  Через 1-2 минуты проверьте метрики:
    ```bash
    kubectl top nodes
    kubectl top pods
    ```

#### 4. Настройка Horizontal Pod Autoscaler (HPA)

1.  Создайте HPA для вашего Deployment:
    ```bash
    kubectl autoscale deployment postgres-deployment --cpu-percent=50 --min=2 --max=5
    ```
2.  Проверьте статус HPA:
    ```bash
    kubectl get hpa
    ```

#### 5. Установка Prometheus и Grafana

1.  Установите Helm:
    ```bash
    sudo snap install helm --classic
    ```
2.  Добавьте репозиторий и установите `kube-prometheus-stack`:
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    helm install prometheus prometheus-community/kube-prometheus-stack
    ```
3.  Дождитесь запуска подов:
    ```bash
    kubectl get pods -w
    ```

#### 6. Работа с minikube на удаленном сервере

Если ваш minikube развернут на удаленном сервере, вам необходимо настроить `port-forwarding`

```bash
kubectl port-forward --address 0.0.0.0 svc/prometheus-grafana 3000:80
# на стороне удаленного сервера
```

```bash
ssh -L 9090:localhost:9090 -L 3000:localhost:3000 pris-server 
# на стороне вашего пк
```

```bash
kubectl port-forward --address 0.0.0.0 svc/prometheus-kube-prometheus-prometheus 9090:9090
# на стороне удаленного сервера

```

#### 7. Настройка дашбордов в Grafana

1.  Сделайте Grafana доступной через NodePort:
    ```bash
    kubectl patch svc prometheus-grafana -p '{"spec": {"type": "NodePort"}}'
    kubectl get svc prometheus-grafana # Запомните порт NodePort (например, 31234)
    ```
2.  Откройте Grafana в браузере: `http://<MINIKUBE_IP>:<NODEPORT>` (например, `http://192.168.49.2:31234`). Получите IP через `minikube ip`.
3.  Войдите в Grafana:
    *   **Username:** `admin`
    *   **Password:**
      ```bash
      kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
      ```
4.  Проверьте Data Source Prometheus (обычно уже настроен).
5.  Импортируйте дашборд:
    *   В левом меню: "+" -> "Import".
    *   Введите ID дашборда, например, `315` (Kubernetes Cluster Monitoring) или `9628` (PostgreSQL Database).
    *   Нажмите "Load".
    *   Выберите Data Source "Prometheus".
    *   Нажмите "Import".

## Lab 2

### Цель

ознакомиться с микросервисной архитектурой, работой с GraphQL API и Apollo Federation

### Задачи

В рамках реализации лабораторной работы было решено использовать

### Инструкция

#### 1. Развертывание сервисов хранения данных

Создайте docker-compose  файл, в котором будет создваться PostgreSQL север и MongoDB

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: service_user
      POSTGRES_PASSWORD: pgpassword
      POSTGRES_DB: graphql_demo
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres_user -d myapp_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:5.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongo_user
      MONGO_INITDB_ROOT_PASSWORD: mongopassword
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5
```

#### 2. Проектирование микросервисов

В рамках задачи было решено реализовывать сервисы, отражающие процесс работы внедора IT продукта: Сущность Customers отвечает за хранение и взаимодействие с информацией по клиентам, Licenses - по-сути справочник лицензий, или переработанный прайс продукта. Access - выдача лицензии клиенту вместе с доступом к пакетному репозиторию ПО

#### 3. Создание микросервисов

Согласно заданию в каждом сервисе были реализованы файлы:
* `db.py`, содержащий подключение к хранилищу и обработку запросов к нему
* `schema.py`, содержащий описание сущностей и запросов Strawberry GraphQL
* `resolvers.py` - связывающий слой между db и schema, задача которого - резолвить запросы и мутации из schema и запрашивать соответствующие функции из db
* `main.py`, содержащий все необходимое, для запуска сервиса

#### 4. Создание Dockerfile

Создайте в каждом сервисе `Dockerfile`, содержащий необходимые команды для корректной работы сервиса в докер контейнере. Например

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/access/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4003"]
```

#### 5. Настройка Apollo Federation

Создайте рядом с директорией `services/`, хранящей папки со всеми сервисами, директорию `gateway`. В данной директории должны находится файлы `gateway.js` и `package.json`, с настройками Apollo

gateway.js:

```js
const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'customers', url: 'http://customers:4001/graphql' },
      { name: 'licenses', url: 'http://licenses:4002/graphql' },
      { name: 'access', url: 'http://access:4003/graphql' },
    ],
  }),
});

const server = new ApolloServer({
  gateway,
  introspection: true,
});

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`Gateway ready at ${url}`);
});
```

**Важно!** в данном файле прописываются субграфы, в которых будут распологаться API созданных ранее сервисов. Необходимо указать здесь все названия и ссылки на сервисы

package.json

```json
{
  "name": "gateway",
  "version": "1.0.0",
  "main": "gateway.js",
  "scripts": {
    "start": "node gateway.js"
  },
  "dependencies": {
    "@apollo/gateway": "^2.9.3",
    "@apollo/server": "^4.9.3",
    "graphql": "^16.8.1"
  }
}
```

Также в данной директории должен находиться `Dockerfile` для Apollo:

```
FROM node:18-alpine

WORKDIR /app

COPY gateway/package*.json ./
RUN npm install

COPY gateway/ .

EXPOSE 4000

CMD ["npm", "start"]
```

#### 6. Запуск и проверка корректности работы

Перед запусом контейнеров необходимо добавить все сервисы (в том числе gateway) в `docker-compose.yaml`:

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: service_user
      POSTGRES_PASSWORD: pgpassword
      POSTGRES_DB: graphql_demo
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres_user -d myapp_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:5.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongo_user
      MONGO_INITDB_ROOT_PASSWORD: mongopassword
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5

  customers:
    build:
      context: .
      dockerfile: services/customers/Dockerfile
    ports:
      - "4001:4001"
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://service_user:pgpassword@postgres:5432/graphql_demo

  licenses:
    build:
      context: .
      dockerfile: services/licenses/Dockerfile
    ports:
      - "4002:4002"
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://service_user:pgpassword@postgres:5432/graphql_demo

  access:
    build:
      context: .
      dockerfile: services/access/Dockerfile
    ports:
      - "4003:4003"
    depends_on:
      - mongodb
    environment:
      - MONGODB_URL=mongodb://mongo_user:mongopassword@mongodb:27017/access_db?authSource=admin

  gateway:
    build:
      context: .
      dockerfile: gateway/Dockerfile
    ports:
      - "4000:4000"
    depends_on:
      - customers
      - licenses
      - access
    environment:
      - NODE_ENV=development
    #restart: on-failure

volumes:
  postgres_data:
  mongo_data:
```

Для запуска всех контейнеров можно использовать:

```sh
docker-compose up -d --build
```

После того как все контейнеры были успешно запущены, можно проверить работу API сервисов отдельно и API всей федерации

Например для сервиса `customers`:

```url
http://localhost:4001/graphql
``` 

Пример запроса:

```graphql
mutation {
  createCustomer(customerData:
  	{
      name: "asdfsd",
      description: "asdasdfryttjhgfdewqergt",
      inn: 156874
    }
  ) {
    id
  }
}
```

Для проверки работы Apollo и федерации:

```url
http://localhost:4000/
```

Пример федеративного запроса:

```
{
  getAccessRecord(id: "68d45627745527d9d9d7939c") {
    id
    repoUname
    customer {
      id
      name
      inn
    }
    license {
      id
      name
      type
    }
  }
}
```

## Lab 3


### Цель
Разработать веб-приложение на Flask, интегрированное с кластером Apache Spark, для загрузки, анализа и визуализации больших CSV-датасетов, а также обучения модели машинного обучения (линейная регрессия).


### Архитектура
- **Flask** — веб-интерфейс и Spark Driver.
- **Spark Standalone Cluster** (в Docker):
  - `spark-master` (UI на порту 8080),
  - `spark-worker` — для распределённых вычислений.
- **Общий Docker-том** (`shared-data`) — обмен файлами между Flask и Spark.
- **Запуск** через `docker-compose`.


### Технологии
- Python 3.11, Flask, PySpark 3.5+
- Docker, docker-compose
- Matplotlib, Pandas (только для визуализации на стороне драйвера)
- Apache Spark Standalone (внешний кластер)

## Структура проекта

```
bigdata-app/
├── app.py # Flask-приложение
├── spark_service.py # Логика анализа и ML с PySpark
├── templates/
│ ├── index.html # Загрузка файла
│ └── results.html # Результаты анализа
├── docker-compose.yml
├── Dockerfile (Flask)
└── shared/ # Общий том (upload/results)
```

### Основные этапы реализации

#### 1. **Загрузка и обработка данных**
- CSV-файл загружается через веб-интерфейс во временный каталог.
- PySpark читает файл **без `inferSchema`**, чтобы избежать ошибок с пропусками (`"NA"`).
- Числовые колонки явно приводятся к типу `DoubleType`.
- Строки с отсутствующим `SalePrice` удаляются.

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Файл не выбран')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('Файл не выбран')
        return redirect('/')
    if file and file.filename.endswith('.csv'):
        filename = f"{uuid.uuid4().hex}.csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('analyze', filename=filename))
    else:
        flash('Поддерживаются только CSV-файлы')
        return redirect('/')


@app.route('/analyze/<filename>')
def analyze(filename):
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(input_path):
        flash('Файл не найден')
        return redirect('/')

    result_id = str(uuid.uuid4())
    result_dir = os.path.join(app.config['RESULT_FOLDER'], result_id)
    os.makedirs(result_dir, exist_ok=True)

    try:
        results = analyze_dataset(input_path, result_dir)

        return render_template(
            'results.html',
            filename=filename,
            schema=results['schema'],
            row_count=results['row_count'],
            column_count=results['column_count'],
            sample=results['sample_html'],
            summary_file=f"{result_id}/{results['summary_file']}",
            plot_file=f"{result_id}/{results['plot_file']}" if results['plot_file'] else None,
            model_metrics=results.get('model_metrics'),  # ← добавь это
            prediction_plot=f"{results['prediction_plot']}" if results.get('prediction_plot') else None,
            _result_id=result_id
        )
    except Exception as e:
        flash(f"Ошибка при анализе: {str(e)}")
        return redirect('/')
```

Файл `spark_service.py`:

```pyhton
import os
import sys
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, isnan
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import DoubleType


def analyze_dataset(input_path: str, result_dir: str, spark_master_url: str = "local[*]") -> dict:
    spark = SparkSession.builder \
        .appName("HousePricePrediction") \
        .master(spark_master_url) \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()


    try:
        # === 1. Загрузка данных ===
        df = spark.read.option("header", "true").csv(input_path)  # inferSchema=False — будем сами управлять типами

        schema = df.dtypes
        row_count = df.count()
        column_count = len(df.columns)

        plot_filename = None

        numeric_columns = [
            "OverallQual", "GrLivArea", "GarageCars", "TotalBsmtSF",
            "1stFlrSF", "FullBath", "TotRmsAbvGrd", "YearBuilt", "SalePrice"
        ]

        print(f"Initial rows: {row_count}", flush=True)

        for col_name in numeric_columns:
            if col_name in df.columns:
                df = df.withColumn(col_name, col(col_name).cast(DoubleType()))

        df = df.filter(col("SalePrice").isNotNull())

        print(f"After filtering SalePrice not null: {df.count()}", flush=True)

        sample_pdf = df.limit(10).toPandas()
        summary_pdf = df.describe().toPandas()
        summary_filename = "summary.csv"
        summary_pdf.to_csv(os.path.join(result_dir, summary_filename), index=False)

        numeric_cols = [name for name, typ in df.dtypes
                        if typ == 'double' and name != 'SalePrice']

        if not numeric_cols:
            return {
                "model_metrics": {"error": f"После преобразования не найдено числовых признаков. Типы: {df.dtypes}"}
            }

        feature_cols = numeric_cols
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
        df_model = assembler.transform(df).select("features", "SalePrice")

        print(f"After VectorAssembler (non-null features): {df_model.count()}", flush=True)

        train_data, test_data = df_model.randomSplit([0.8, 0.2], seed=42)

        print(f"Train size: {train_data.count()}, Test size: {test_data.count()}", flush=True)

        lr = LinearRegression(featuresCol="features", labelCol="SalePrice")
        lr_model = lr.fit(train_data)

        predictions = lr_model.transform(test_data)

        evaluator = RegressionEvaluator(labelCol="SalePrice", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        r2 = RegressionEvaluator(labelCol="SalePrice", predictionCol="prediction", metricName="r2").evaluate(predictions)

        saleprice_pdf = df.select("SalePrice").dropna().toPandas()
        if not saleprice_pdf.empty and len(saleprice_pdf) > 0:
            plt.figure(figsize=(8, 5))
            plt.hist(saleprice_pdf["SalePrice"], bins=30, color='skyblue', edgecolor='black')
            plt.title("Распределение целевой переменной (SalePrice)")
            plt.xlabel("Цена продажи")
            plt.ylabel("Частота")
            plot_filename = f"{uuid.uuid4().hex}_saleprice_hist.png"
            plt.savefig(os.path.join(result_dir, plot_filename), bbox_inches='tight')
            plt.close()
        else:
            plot_filename = None

        pred_pdf = predictions.select("SalePrice", "prediction").dropna().limit(200).toPandas()
        pred_plot_filename = None
        if not pred_pdf.empty:
            plt.figure(figsize=(8, 6))
            plt.scatter(pred_pdf["SalePrice"], pred_pdf["prediction"], alpha=0.6, color='purple')
            min_val = min(pred_pdf["SalePrice"].min(), pred_pdf["prediction"].min())
            max_val = max(pred_pdf["SalePrice"].max(), pred_pdf["prediction"].max())
            plt.plot([min_val, max_val], [min_val, max_val], 'r--')
            plt.xlabel("Реальная цена")
            plt.ylabel("Предсказанная цена")
            plt.title(f"Предсказания модели (RMSE: {rmse:.2f}, R²: {r2:.2f})")
            pred_plot_filename = f"{uuid.uuid4().hex}_pred.png"
            plt.savefig(os.path.join(result_dir, pred_plot_filename), bbox_inches='tight')
            plt.close()

        return {
            "schema": schema,
            "row_count": row_count,
            "column_count": column_count,
            "sample_html": sample_pdf.to_html(classes='table table-striped', escape=False),
            "summary_file": summary_filename,
            "plot_file": plot_filename,
            "model_metrics": {
                "rmse": round(rmse, 2),
                "r2": round(r2, 2)
            },
            "prediction_plot": pred_plot_filename
        }

    finally:
        spark.stop()
```

#### 2. **Анализ и визуализация**
- Генерируется сводная статистика (`df.describe()` → `summary.csv`).
- Строится гистограмма распределения целевой переменной (`SalePrice`).
- Пример данных отображается в HTML-таблице.

#### 3. **Машинное обучение**
- Используется `VectorAssembler` для формирования вектора признаков.
- Обучается модель **линейной регрессии** (`LinearRegression`).
- Оцениваются метрики: **RMSE** и **R^2**.
- Строится график «реальные vs предсказанные значения».

#### 4. **Интеграция с веб-интерфейсом**
- Результаты (графики, таблицы, метрики) отображаются на странице `results.html`.
- Файлы хранятся в изолированной директории по UUID, чтобы избежать конфликтов.

### Как запустить
```bash
git clone <repo>
cd bigdata-app
docker-compose up -d --build
```

Затем зайти на

```
http://localhost:5001/
```












