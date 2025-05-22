from odoo import models, fields

class OtherCostSet(models.Model):
    _name = 'sample_template.other_cost_set'
    _description = 'Reusable Other Cost Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")

    other_cost_line_ids = fields.One2many(
        'sample_template.other_cost_line',
        'set_id',
        string="Other Cost Lines"
    )