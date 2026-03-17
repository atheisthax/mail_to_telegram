FROM python:3-slim
RUN useradd -m appuser
USER appuser
WORKDIR /opt/mail_to_telegram
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8465
CMD [ "python", "mail_to_telegram.py" ]
