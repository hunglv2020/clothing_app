# models/spec_image.py
from odoo import models, fields

class SpecImage(models.Model):
    _name = 'sample_template.spec_image'
    _description = 'Specification Image'
    _order = 'sequence'

    name = fields.Char(string="Title / Label")
    image = fields.Binary(string="Image", store=True)
    note = fields.Text(string="Description")
    specification_id = fields.Many2one(
        'sample_template.specification',
        string="Specification",
        ondelete="set null"
    )
    sequence = fields.Integer(default=10)

    def action_unlink_self_from_specification(self):
        for record in self:
            record.specification_id = False