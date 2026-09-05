from marshmallow import Schema, fields, validate

class JobCreateSchema(Schema):
    name = fields.String(required=True)
    status = fields.String(required=True,
                           validate=validate.OneOf([
                               "running",
                               "finished",
                               "canceled"
                           ]))
    source = fields.String(required=True)
    description = fields.String(required=False, allow_none=True)
    
class JobResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    status = fields.String()
    source = fields.String()
    description = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
class JobReplaceSchema(Schema):
    name = fields.Str(required=True)
    status = fields.String(required=True,
                            validate=validate.OneOf([
                                "running",
                                "finished",
                                "canceled"
                            ]))
    source = fields.Str(required=True)
    description = fields.Str(required=False)
    
class JobUpdateSchema(Schema):
    name = fields.Str(required=False)
    status = fields.String(required=False,
                            validate=validate.OneOf([
                                "running",
                                "finished",
                                "canceled"
                            ]))
    source = fields.Str(required=False)
    description = fields.Str(required=False)    