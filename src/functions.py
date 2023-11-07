import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

# Получаем данные для SMTP сервера из переменных окружения
SMTP_HOST = os.environ.get('smtp_ya_host')
SMTP_MAIL = os.environ.get('smtp_ya_mail')
SMTP_PASSWORD = os.environ.get('smtp_ya_password')
SMTP_PORT = int(os.environ.get('smtp_ya_port'))


def send_mail(to_addr, subject, text):
    """
    Функция для отправки электронных писем.
    """
    # Создаем объект сообщения
    msg = MIMEMultipart()
    msg['From'] = 'new.gres@yandex.ru'
    msg['To'] = to_addr
    msg['Subject'] = subject

    # Добавляем текст сообщения
    msg.attach(MIMEText(text, 'plain'))

    # Подключаемся к SMTP серверу и отправляем сообщение
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_MAIL, SMTP_PASSWORD)
        server.send_message(msg)


def generate_password(length):
    """
    Функция для генерации случайного пароля указанной длины.
    """
    # Список возможных символов для пароля
    characters = string.ascii_letters + string.digits + string.punctuation

    # Генерируем пароль
    password = ''.join(random.choice(characters) for _ in range(length))

    return password
