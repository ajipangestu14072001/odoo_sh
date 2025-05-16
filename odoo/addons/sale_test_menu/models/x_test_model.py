from odoo import models, fields

class XTestModel(models.Model):
    _name = 'x_test.model'
    _description = 'Test Model'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
