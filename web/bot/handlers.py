# TODO добавить логирование
import requests
from schema import ResponseSchema
from  marshmallow.exceptions import ValidationError

schema = ResponseSchema()


def error_message(update, context, message="Произошла ошибка при загрузке фото. Попробуйтеещё раз."):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def wolfram_quary(update, context, expr):
    pass


def start(update, context, user_data):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот, который умет распознавать '
                                                                    'написанное от руки математического выражения '
                                                                    'и преобразовывать его в запрос к WolframAlpha.'
                                                                    ' Чтобы попробовать, пришлите мне'
                                                                    ' фотографию написанного выражения.')


def photo(update, context, user_data):
    file_info = context.bot.get_file(update.message.photo[-1].file_id)
    file = context.bot.download_file(file_info.file.path)
    r = requests.post('http://127.0.0.1:5000/photos',
                      files={"photo": file}, data={"image_id": str(update.message.massage_id)})
    if r.status_code != 200:
        error_message(update, context)
        return
    r = requests.get(f'http://127.0.0.1:5000/photos/{update.message.massage_id}')
    try:
        s = schema.load(r.content)
        expr = s['expression']
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы ввели выражение: {expr}")
        wolfram_quary(update, context, expr)
    except ValidationError:
        error_message(update, context)


def unknown(update, context, user_data):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, но я Вас не понимаю. Если вы хотите,"
                                                                    "чтобы я нашел значение рукописного выражения,"
                                                                    "просто пришлите мне его фото")
