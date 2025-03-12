import telebot
from telebot import types
import pickle
import Core.Run
import GoidaMetr
#
# import aicore




trustedusers = ["EmikaMeleda", "cold_goat"]

# Защита от посторонних
def trust(func):
    def inner1(*args, **kwargs):
        username = args[0].chat.username
        print(f'USERNAME: {username}')
        if username in trustedusers:
            print("TRUSTED")
            func(*args, **kwargs)
        else:
            print("UNTRUSTED USER")
    return inner1



# Токен из файла
def getToken():
    with open('anastasiya.token', 'rb') as f:
        return pickle.load(f)


# бот
bot = telebot.TeleBot(getToken())

# /start и /help
@bot.message_handler(commands=['start', 'help'])
@trust
def send_welcome(message):
    #print(message.chat.id)
    bot.reply_to(message, "гооол")


# бомбер
@bot.message_handler(commands=['bomber'])
@trust
def bomber(message):
    arg = list(message.text.split())[1:]
    if arg[0] == 'group':
        numbers = arg[2:int(arg[1])+2]
    else:
        numbers = [arg[1]]
    attacktype = arg[-3].upper()
    feedback = bool(arg[-2])
    attacknum = arg[-1]
    print(numbers, attacktype, attacknum)
    bot.send_message(message.chat.id, "Хуярю пидорасво...")
    try:
        Core.Run.start_async_attackvx(numbers, attacktype, feedback, attcknum)
    except Exception:
        bot.send_message(message.chat.id, str(Exception))
    bot.send_message(message.chat.id, f"ЗАХУЯРИЛ ПИДОРАС{'А' if arg[0] == 'single' else 'ОВ'} АХАХ")


# гойдометр
@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('audio/user_voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    result = GoidaMetr.analyze('user_voice.ogg')
    rate = result[1]

    finalstring = ""

    finalstring = f"Гойдометр v2 by EmikaMeleda\n\n[{str(round(rate, 9-len(str(int(rate)))))+'0'*(10-len(str(round(rate, 9-len(str(int(rate)))))))}]\n\n[{round(result[2], 9-len(str(int(result[2]))))} гойд/с]"
    

    bot.send_message(message.chat.id, finalstring)


# ai
#@bot.message_handler()
#@trust
#def aimessages(message):
    #history = message.chat.
    

    




bot.infinity_polling()
