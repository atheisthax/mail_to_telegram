# mail_to_telegram
resend smtp messages to telegram with images

!Important!
create config.py to load chat_id and bot_token variables to code
it looks like:

bot_token = '123123123123:SdfSDFsdfSDfWdeyfM-123SDFSDFsdf-O6df'
chat_id = '12321343454'

It opens SMTP listener on 1025 port and 0.0.0.0 address and resend all emails to telegram via bot.
