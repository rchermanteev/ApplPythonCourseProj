from app import app
import time
import os
from sqlalchemy.orm import sessionmaker
from models import engine, Image
from flask import request, abort
from logger_config import LOGGING_CONFIG
import logging.config
import validation
from marshmallow.exceptions import ValidationError

PHOTO_DIR = 'images/'
Session = sessionmaker(bind=engine)
logger = logging.getLogger('RequestLogger')
logging.config.dictConfig(LOGGING_CONFIG)
logger.info('App running')
schema = validation.ImageSchema()
app.config['UPLOAD_FOLDER'] = PHOTO_DIR


@app.route('/photos', methods=['POST'])
def post_photo():
    try:
        js = schema.load(request.json)
        image_id = js['image_id']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image_id)
        file = request.files['photo']
        if file:
            file.save(path)
            session = g.session
            item = Image(id=image_id, path=path, result=None)
            session.add(item)
            session.commit()
            return 'OK'
        abort(400, 'Missing file')
    except ValidationError as e:
        abort(400, str(e))


@app.route('/photos/<int:image_id>/', methods=['GET'])
def get_result(image_id):
    """возврашаем строку запроса"""
    return 'not implemented'


@app.before_request
def before_request():
    g.start = time.time()
    g.session = Session()


@app.after_request
def after_request(response):
    resp_time = (time.time() - g.start) * 1000  # время ответа сервера в миллисекндах
    logger.info('%s %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                response.status, resp_time)
    g.session.close()
    return response
