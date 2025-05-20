from odoo import models, fields

class OperationSet(models.Model):
    _name = 'sample_template.operation_set'
    _description = 'Reusable Operation Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")
    
    operation_line_ids = fields.One2many(
        'sample_template.operation_line',
        'operation_set_id',
        string="Operation Lines"
    )
