# Используем официальный образ PostgreSQL
FROM postgres:latest

# Устанавливаем переменные окружения (можно перезаписать при запуске)
ENV POSTGRES_DB=mobile_dev
ENV POSTGRES_USER=entityfrm
ENV POSTGRES_PASSWORD=pP3VJsoAcX2q

# Копируем скрипт инициализации (если есть)
COPY init.sql /docker-entrypoint-initdb.d/

# Объявляем объем для данных (чтобы данные сохранялись между запусками)
VOLUME /var/lib/postgresql/data

# Указываем порт
EXPOSE 5432
