from app import app


@app.route('/photos', methods=['POST'])
def post_photo():
    """сохраняем файл с изображением и пишем в базу данных путь к нему, возвращаем пользователю id"""
    return 'OK'


@app.route('/photos/<int:image_id>/', methods=['GET'])
def get_result(image_id):
    """возврашаем строку запроса"""
    return 'not implemented'

