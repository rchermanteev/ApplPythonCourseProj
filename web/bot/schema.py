from marshmallow import Schema, fields


class ResponseSchema(Schema):
    image_id = fields.String(required=True)
