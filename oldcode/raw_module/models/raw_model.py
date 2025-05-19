from odoo import models, fields

class RawModel(models.Model):
    _name = 'raw.model'
    _description = 'Raw Model'

    name = fields.Char(string='Name', required=True)
