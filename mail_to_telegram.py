import base64
import logging.handlers
import mailparser
import telebot
from aiosmtpd.controller import Controller
import config
import time

class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content         # type: bytes
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
        return '250 OK'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("python-mail_to_telegram")
    logging.info("Started on %s:%s..." % (config.listen_addr, config.listen_port))
    handler = CustomHandler()
    controller = Controller(handler, hostname=config.listen_addr, port=int(config.listen_port))
    # Run the event loop in a separate thread.
    controller.start()
    # Wait for the user to press Return.
    #input('SMTP server running. Press Return to stop server and exit.')
    while True:
        time.sleep(1000)
    controller.stop()
