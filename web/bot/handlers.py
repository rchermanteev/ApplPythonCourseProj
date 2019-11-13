# TODO добавить логирование
import requests
from schema import ResponseSchema
from wolfram_api import WolfQueryException, api_query
from logger import logger
from time import time
import json

schema = ResponseSchema()


def error_message(update, context, message="Произошла ошибка. Попробуйте ещё раз."):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот, который умет распознавать '
                                                                    'написанное от руки математического выражения '
                                                                    'и преобразовывать его в запрос к WolframAlpha.'
                                                                    ' Чтобы попробовать, пришлите мне'
                                                                    ' фотографию написанного выражения.')
    logger.info('%s %s %s %s %s %s', 'START_HANDLER', update.update_id, update.message.massage_id,
                update.message.from_user, update.message.date, update.message.text)


def photo(update, context):
    start_time = time()

    file_info = context.bot.get_file(update.message.photo[-1].file_id)
    file = context.bot.download_file(file_info.file.path)
    r = requests.post('http://127.0.0.1:5000/photos',
                      files={"photo": file}, data={"image_id": str(update.message.massage_id)})
    if r.status_code != 200:
        error_message(update, context)
        logger.error('%s %s %s %s', 'PHOTO_HANDLER', update.update_id, "Incorrect server response", r.text)
        return
    r = requests.get(f'http://127.0.0.1:5000/photos/{update.message.massage_id}')
    try:
        s = json.load(r.text)
        expr = s['expression']
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы ввели выражение: {expr}")
        text, img_urls = api_query(expr)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Результат: \n {text}")
        for url in img_urls:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
        resp_time = (time.time() - g.start) * 1000
        logger.info('%s %s %s %s %s %s', 'PHOTO_HANDLER', update.update_id, update.message.massage_id,
                    update.message.from_user, update.message.date, expr, resp_time)
    except (json.JSONDecodeError, WolfQueryException) as e:
        error_message(update, context)
        logger.error('%s %s %s %s', 'PHOTO_HANDLER', update.update_id, "Incorrect wolfram response", str(e))


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, но я Вас не понимаю. Если вы хотите,"
                                                                    "чтобы я нашел значение рукописного выражения,"
                                                                    "просто пришлите мне его фото")
    logger.info('%s %s %s %s %s %s', 'UNKNOWN_HANDLER', update.update_id, update.message.massage_id,
                update.message.from_user, update.message.date, update.message.text)