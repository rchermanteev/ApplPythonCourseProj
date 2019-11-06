# TODO добавить логирование


def start(update, context, user_data):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот, который умет распознавать '
                                                                    'написанное от руки математического выражения '
                                                                    'и преобразовывать его в запрос к WolframAlpha.'
                                                                    ' Чтобы попробовать, пришлите мне'
                                                                    ' фотографию написанного выражения.')


def photo(update, context, user_data):
    pass


def unknown(update, context, user_data):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, но я Вас не понимаю. Если вы хотите,"
                                                                    "чтобы я нашел значение рукописного выражения,"
                                                                    "просто пришлите мне его фото")
