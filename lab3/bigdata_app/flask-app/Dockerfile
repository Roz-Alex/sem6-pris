# flask-app/Dockerfile
FROM python:3.11-slim

# Устанавливаем OpenJDK 21 (единственный доступный в Debian trixie)
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Указываем JAVA_HOME для Spark
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PYSPARK_PYTHON=python3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /shared/upload /shared/results

EXPOSE 5000

CMD ["python", "app.py"]