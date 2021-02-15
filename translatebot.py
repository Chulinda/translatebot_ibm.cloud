from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import telebot


apikey = 'Kv3NQpS_2m1V9brUEFwmHsLkWYMpWQTVWGI7kvexycfT'
url = 'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/7f50c216-38d3-4ffd-9e09-06bdeab479e8'
bot = telebot.TeleBot('1674770642:AAFi2fGd1B7A3bUj5z9e-6MfeohEUho9Mok')

authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
lt.set_service_url(url)

def trans(word, id):
    global translation
    try:
        translation = lt.translate(text=word, model_id=id).get_result()
    except :
        pass

    translation = translation['translations'][0]['translation']



@bot.message_handler(commands=["id"])
def link(message):
    msg = bot.send_message(message.chat.id, 'Введите перевод (en-ru или ru-en)')
    bot.register_next_step_handler(msg, search)



@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, Натали, воспользуйся командой /id для установки парметров перевода.')


@bot.message_handler(content_types = ['text'])
def main(message):
    global id
    trans(message.text, id)
    bot.send_message(message.chat.id, translation)

def search(message):
    global id
    if message.text == 'ru-en':
        id = 'ru-en'
        bot.send_message(message.chat.id, 'Теперь вводите предложения на русском')
    elif message.text == 'en-ru':
        id = 'en-ru'
        bot.send_message(message.chat.id, 'Теперь вводите предложения на английском')
    else:
        bot.send_message(message.chat.id, 'Не верный ввод')
    
    


if __name__ == '__main__':
    bot.polling()