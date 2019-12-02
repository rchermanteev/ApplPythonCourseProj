import time
import os
import logging.config
from sqlalchemy.orm import sessionmaker
from flask import request, abort, jsonify, g, send_file
from marshmallow.exceptions import ValidationError
import requests

from aplication import app
from aplication.models import engine, Image
from aplication.logger_config import LOGGING_CONFIG
import aplication.validation
from aplication.image_processing import ImageProcessor

PHOTO_DIR = 'images/'
OUTPUT_DIR = 'out_images/'
SERVER_LOCATION = '/home/cloud/ApplPythonCourseProj/web/server'

Session = sessionmaker(bind=engine)
logger = logging.getLogger('RequestLogger')
logging.config.dictConfig(LOGGING_CONFIG)
logger.info('App running')
schema = aplication.validation.ImageSchema()
app.config['UPLOAD_FOLDER'] = PHOTO_DIR
app.config['OUT_FOLDER'] = OUTPUT_DIR


def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db


@app.route('/photos', methods=['POST'])
def post_photo():
    try:
        s = schema.load(request.form)
        image_id = s['image_id']
        img_url = s['img_url']
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(image_id))
        path = path + '.jpg'
        file = requests.get(img_url).content
        if file:
            with open(path, 'wb') as f:
                f.write(file)
            session = get_db()
            item = Image(id=image_id, path=path, result=None, out_path=None)
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
    out_path = os.path.join(app.config['OUT_FOLDER'], str(image_id))
    out_path = out_path + '.jpg'
    image_processor = ImageProcessor(item.path, out_path)
    result = image_processor.run()
    item.result = result
    logger.info('%s', out_path)
    item.out_path = out_path

    session.add(item)
    session.commit()
    return jsonify({'expression': result})


@app.route('/segmentation/<int:image_id>/', methods=['GET'])
def get_segmentation(image_id):
    session = get_db()
    item = session.query(Image).get(image_id)
    if item is None:
        abort(404, "Unexciting image id")
    path = item.out_path
    if path is None:
        abort(404, "Image not found")
    f = os.path.join(SERVER_LOCATION, path)
    return jsonify({'photo': f})


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
