from marshmallow import Schema, fields


class ImageSchema(Schema):
    image_id = fields.Integer(required=True)
