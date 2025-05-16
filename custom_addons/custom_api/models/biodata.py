from odoo import models, fields

class CustomBiodata(models.Model):
    _name = 'custom.biodata'
    _description = 'Custom Biodata'

    name = fields.Char(required=True)
    email = fields.Char(required=True)
    age = fields.Integer(required=True)
