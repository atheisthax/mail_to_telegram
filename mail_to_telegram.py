import asyncore
import base64
import smtpd
import logging.handlers

import mailparser
import telebot

import config

listen_addr = '0.0.0.0'
listen_port = 1025


class mail_to_telegram(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        mail = mailparser.parse_from_bytes(data)
        # if mail have html data - send it
        if len(mail.text_html) > 0:
            message = mail.text_html[0]
        # if mail have plaintext data - send it
        if len(mail.text_plain) > 0:
            message = mail.text_plain[0]
        if message.find("<br/>") > 0:
            message = message[0:message.find("<br/>")]
        message = mail.mail['subject'] + '\n' + message
        bot = telebot.TeleBot(config.bot_token)
        logging.info(message)
        # if mail have attachments - send each one with message from mail
        if len(mail.attachments) > 0:
            for attach in mail.attachments:
                # decode attachment from base64
                image = base64.decodebytes(attach['payload'].encode('utf-8'))
                bot.send_photo(chat_id=config.chat_id, photo=image, caption=message)
        else:
            # if no attachments - send only text message
            bot.send_message(chat_id=config.chat_id, text=message)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python-mail_to_telegram")
server = mail_to_telegram((listen_addr, int(listen_port)), None)
logging.info("Started on %s:%s..." % (listen_addr, listen_port))

try:
    asyncore.loop()
except KeyboardInterrupt:
    logging.info("Keyboard interrupt, exiting")
    pass
