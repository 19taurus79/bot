FROM python:3.11-alpine3.17
LABEL maintainer='Onyshchenko Serhii <19taurus79@gmail.com>'

ARG UID=1000
ARG GID=1000
ENV USER=docker_user

# --- Улучшение #1: Более корректное создание пользователя и домашней директории ---
# adduser -S -h /home/${USER} ${USER} : создает системного пользователя с явно указанной домашней директорией.
# mkdir -p /home/${USER}/app : Убедимся, что директория для приложения существует.
# chown ${USER}:${USER} /home/${USER}/app : Устанавливаем владельца для директории приложения.
RUN adduser -S -h /home/${USER} ${USER} \
    && mkdir -p /home/${USER}/app \
    && chown ${USER}:${USER} /home/${USER}/app

WORKDIR /home/${USER}/app # Теперь эта директория точно принадлежит нашему пользователю.

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# --- Улучшение #2: Добавление --no-cache и очистка кэша APK ---
# --no-cache: не сохраняет кэш пакетов.
# rm -rf /var/cache/apk/*: удаляет временные файлы APK после установки, уменьшая размер образа.
RUN apk update \
    && apk add --no-cache gcc python3-dev musl-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# --- Улучшение #3: Переключение на непривилегированного пользователя ---
# Это ОЧЕНЬ ВАЖНО для безопасности: приложение не будет работать от root.
USER ${USER}

CMD ["python3", "-m", "main_bot"]
