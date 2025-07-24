# Используем официальный образ Python
FROM python:3.12

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . /app/