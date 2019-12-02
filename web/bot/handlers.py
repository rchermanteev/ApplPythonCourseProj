import requests
from wolfram_api import WolfQueryException, api_query
from logger import logger
from time import time
import json
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

keyboard = [['Вернуться назад'], ['Продолжить']]
reply_markup = ReplyKeyboardMarkup(keyboard)
remove_reply_markup = ReplyKeyboardRemove()


def error_message(update, context, message="Произошла ошибка. Попробуйте ещё раз."):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def start(update, context):
    logger.info('%s %s %s %s %s %s', 'START_HANDLER', update.update_id, update.message.message_id,
                update.message.from_user, update.message.date, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Привет {update.message.from_user.first_name}! Я бот, который умет распознавать '
                                                                    'написанное от руки математического выражения '
                                                                    'и преобразовывать его в запрос к WolframAlpha.'
                                                                    ' Чтобы попробовать, пришли мне'
                                                                    ' фотографию написанного выражения.')


def photo(update, context):
    start_time = time()
    file_info = context.bot.get_file(update.message.photo[-1].file_id)
    file_url = file_info.file_path
    r = requests.post('http://127.0.0.1:8000/photos',
                      data={"image_id": str(update.message.message_id),
                            "img_url": str(file_url)})
    if r.status_code != 200:
        error_message(update, context)
        logger.error('%s %s %s %s', 'PHOTO_HANDLER', update.update_id, "Incorrect server response", r.text)
        return
    r = requests.get(f'http://127.0.0.1:8000/photos/{update.message.message_id}/')
    try:
        s = json.loads(r.text)
        expr = s['expression']
        resp = requests.get(f'http://127.0.0.1:8000/segmentation/{update.message.message_id}/')
        segm_img = json.loads(resp.text)['photo']
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Распознанные символы:")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(segm_img, 'rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы ввели выражение: {expr}",
                                 reply_markup=reply_markup)
        context.user_data['expr'] = expr
        resp_time = (time() - start_time) * 1000
        logger.info('%s %s %s %s %s %s %s', 'PHOTO_HANDLER', update.update_id, update.message.message_id,
                    update.message.from_user, update.message.date, expr, str(resp_time))
    except json.JSONDecodeError as e:
        error_message(update, context)
        logger.error('%s %s %s %s', 'PHOTO_HANDLER', update.update_id, "Incorrect wolfram response", str(e))


def wolfram_request(update, context):
    start_time = time()
    if not context.user_data['expr']:
        error_message(update, context, message="Сначала пришлите фото выражения")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=remove_reply_markup)
        return
    expr = context.user_data['expr']
    try:
        text, img_urls = api_query(expr)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Результат: \n {text}",
                                 reply_markup=remove_reply_markup)
        for url in img_urls:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
        resp_time = (time() - start_time) * 1000
        logger.info('%s %s %s %s %s %s %s', 'WOLFRAM_HANDLER', update.update_id, update.message.message_id,
                    update.message.from_user, update.message.date, expr, str(resp_time))
    except WolfQueryException as e:
        error_message(update, context)
        logger.error('%s %s %s %s', 'WOLFRAM_HANDLER', update.update_id, "Incorrect wolfram response", str(e))


def retry(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Хорошо, давай попробуем ещё раз. Попробуй "
                                                                    "написать неверно распознанные символы так "
                                                                    "чтобы их было проще распознать и отправь мне "
                                                                    "новое фото.",
                             reply_markup=remove_reply_markup)
    logger.info('%s %s %s %s %s %s', 'RETRY_HANDLER', update.update_id, update.message.message_id,
                update.message.from_user, update.message.date, update.message.text)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, но я Вас не понимаю. Если вы хотите,"
                                                                    "чтобы я нашел значение рукописного выражения,"
                                                                    "просто пришлите мне его фото")
    logger.info('%s %s %s %s %s %s', 'UNKNOWN_HANDLER', update.update_id, update.message.message_id,
                update.message.from_user, update.message.date, update.message.text)
