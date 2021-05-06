import asyncore
import base64
import smtpd

import mailparser
import telebot

import config

listen_addr = '0.0.0.0'
listen_port = 1025


class mail_to_telegram(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        mail = mailparser.parse_from_bytes(data)
        message = mail.text_html[0]
        message = message[0:message.find("<br/>")]
        bot = telebot.TeleBot(config.bot_token)
        print(message)
        for attach in mail.attachments:
            image = base64.decodebytes(attach['payload'].encode('utf-8'))
            bot.send_photo(chat_id=config.chat_id, photo=image, caption=message)


server = mail_to_telegram((listen_addr, int(listen_port)), None)
print("Started on %s:%s..." % (listen_addr, listen_port))

try:
    asyncore.loop()
except KeyboardInterrupt:
    pass
