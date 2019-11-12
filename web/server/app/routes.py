from app import app
import time
import os
from sqlalchemy.orm import sessionmaker
from models import engine, Image
from flask import request, abort, jsonify, g
from logger_config import LOGGING_CONFIG
import logging.config
import validation
from marshmallow.exceptions import ValidationError
from image_processing import ImageProcessor

PHOTO_DIR = 'images/'
Session = sessionmaker(bind=engine)
logger = logging.getLogger('RequestLogger')
logging.config.dictConfig(LOGGING_CONFIG)
logger.info('App running')
schema = validation.ImageSchema()
app.config['UPLOAD_FOLDER'] = PHOTO_DIR


def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db


@app.route('/photos', methods=['POST'])
def post_photo():
    try:
        s = schema.load(request.form)
        image_id = s['image_id']
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(image_id))
        file = request.files['photo']
        if file:
            file.save(path)
            session = get_db()
            item = Image(id=image_id, path=path, result=None)
            session.add(item)
            session.commit()
            return 'OK'
        abort(400, 'Missing file')
    except ValidationError as e:
        abort(400, str(e))


@app.route('/photos/<int:image_id>/', methods=['GET'])
def get_result(image_id):
    session = get_db()
    item = session.query(Image).get(image_id)
    if item is None:
        abort(404, "Unexciting image id")
    image_processor = ImageProcessor(item.path)
    result = image_processor.run()
    item.result = result
    session.add(item)
    session.commit()
    return jsonify({'expression': result})


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    resp_time = (time.time() - g.start) * 1000  # время ответа сервера в миллисекндах
    logger.info('%s %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                response.status, resp_time)
    return response


@app.teardown_appcontext
def teardown_db(args):
    db = g.pop('db', None)

    if db is not None:
        db.close()
