FROM python:3

WORKDIR /opt/mail_to_telegram

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "mail_to_telegram.py" ]
